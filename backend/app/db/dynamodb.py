"""DynamoDB client and operations."""
import boto3
import logging
from botocore.exceptions import ClientError
from ..core.config import settings

logger = logging.getLogger(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
dynamodb_client = boto3.client('dynamodb', region_name=settings.AWS_REGION)

# Get table references
users_table = dynamodb.Table(settings.DYNAMODB_USERS_TABLE)
tenants_table = dynamodb.Table(settings.DYNAMODB_TENANTS_TABLE)

async def create_user(user_data: dict) -> dict:
    """Create a new user in DynamoDB."""
    try:
        response = users_table.put_item(Item=user_data)
        return user_data
    except ClientError as e:
        logger.error(f"Error creating user: {e}")
        raise

async def get_user(user_id: str) -> dict:
    """Get a user by ID."""
    try:
        response = users_table.get_item(Key={"id": user_id})
        return response.get("Item")
    except ClientError as e:
        logger.error(f"Error getting user: {e}")
        raise

async def get_user_by_cognito_id(cognito_id: str) -> dict:
    """Get a user by Cognito ID using a secondary index."""
    try:
        response = users_table.query(
            IndexName="CognitoIdIndex",
            KeyConditionExpression="cognito_id = :cognito_id",
            ExpressionAttributeValues={":cognito_id": cognito_id}
        )
        items = response.get("Items", [])
        return items[0] if items else None
    except ClientError as e:
        logger.error(f"Error getting user by Cognito ID: {e}")
        raise

async def create_tenant(tenant_data: dict) -> dict:
    """Create a new tenant in DynamoDB."""
    try:
        response = tenants_table.put_item(Item=tenant_data)
        return tenant_data
    except ClientError as e:
        logger.error(f"Error creating tenant: {e}")
        raise

async def get_tenant(tenant_id: str) -> dict:
    """Get a tenant by ID."""
    try:
        response = tenants_table.get_item(Key={"id": tenant_id})
        return response.get("Item")
    except ClientError as e:
        logger.error(f"Error getting tenant: {e}")
        raise

async def update_user(user_id: str, update_data: dict) -> dict:
    """Update user fields in DynamoDB."""
    try:
        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in update_data.keys())
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}
        response = users_table.update_item(
            Key={"id": user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        return response.get("Attributes")
    except ClientError as e:
        logger.error(f"Error updating user: {e}")
        raise