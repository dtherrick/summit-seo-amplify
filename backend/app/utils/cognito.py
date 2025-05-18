"""Cognito utility functions."""
import json
import logging
import boto3
from jose import jwk, jwt
from jose.utils import base64url_decode
from typing import Dict, Any, Optional
from ..core.config import settings

logger = logging.getLogger(__name__)

# Initialize Cognito client
cognito_idp = boto3.client('cognito-idp', region_name=settings.AWS_REGION)

# Cache for JWKs to avoid repeated fetching
jwks_cache = {}

async def get_jwks(user_pool_id: str) -> Dict:
    """Get the JSON Web Key Set for a Cognito User Pool."""
    global jwks_cache

    if user_pool_id in jwks_cache:
        return jwks_cache[user_pool_id]

    keys_url = f'https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(keys_url)
        keys = response.json()['keys']

    jwks_cache[user_pool_id] = {key['kid']: key for key in keys}
    return jwks_cache[user_pool_id]

async def verify_cognito_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a Cognito JWT token and return its claims if valid."""
    try:
        # Get the key id from the token header
        header = jwt.get_unverified_header(token)
        kid = header['kid']

        # Get the JWKs for our user pool
        jwks = await get_jwks(settings.COGNITO_USER_POOL_ID)

        if kid not in jwks:
            logger.error(f"Key ID {kid} not found in JWKS")
            return None

        # Get the public key for verification
        public_key = jwks[kid]

        # Verify the token
        message, encoded_signature = token.rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        # Construct the key
        key = jwk.construct(public_key)

        # Verify the signature
        if not key.verify(message.encode('utf-8'), decoded_signature):
            logger.error("Signature verification failed")
            return None

        # Get the claims
        claims = jwt.get_unverified_claims(token)

        # Verify the token is not expired
        import time
        if claims['exp'] < time.time():
            logger.error("Token is expired")
            return None

        # Verify the audience (client ID)
        if claims['aud'] != settings.COGNITO_APP_CLIENT_ID:
            logger.error(f"Token was not issued for this client id: {claims['aud']}")
            return None

        return claims

    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return None