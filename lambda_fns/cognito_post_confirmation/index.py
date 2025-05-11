import boto3
import os
import datetime
import uuid

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
# Table name from environment variable. CDK will set this.
USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME')
# It's good practice to ensure critical env vars are present
if not USERS_TABLE_NAME:
    raise EnvironmentError("Missing USERS_TABLE_NAME environment variable")
users_table = dynamodb.Table(USERS_TABLE_NAME)

def handler(event, context):
    """
    Cognito Post-Confirmation Lambda Trigger
    Creates a user profile in DynamoDB after a user confirms their account.
    """
    print(f"Received event: {event}") # Log the incoming event for debugging

    user_attributes = event['request']['userAttributes']
    cognito_username = event['userName']

    cognito_id = user_attributes.get('sub', cognito_username)
    email = user_attributes.get('email')

    if not cognito_id or not email:
        print("Error: Missing 'sub' (cognito_id) or 'email' in userAttributes.")
        # Depending on strictness, you might want to return event or raise error
        return event # Allow Cognito flow to complete

    user_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()

    item = {
        'user_id': user_id,
        'cognito_id': cognito_id,
        'email': email,
        'tenant_id': user_attributes.get('custom:tenant_id'),
        'subscription_tier': user_attributes.get('custom:subscription_tier', 'free'),
        'user_type': user_attributes.get('custom:user_type', 'user'),
        'business_name': user_attributes.get('custom:business_name'),
        'business_website': user_attributes.get('custom:business_website'),
        'business_industry': user_attributes.get('custom:business_industry'),
        'created_at': timestamp,
        'updated_at': timestamp,
    }

    # Remove any keys with None values to avoid DynamoDB validation errors for empty strings
    item_cleaned = {k: v for k, v in item.items() if v is not None}

    try:
        users_table.put_item(Item=item_cleaned)
        print(f"Successfully created user profile for cognito_id: {cognito_id}, user_id: {user_id}. Item: {item_cleaned}")
    except Exception as e:
        print(f"Error creating user profile for cognito_id: {cognito_id}, user_id: {user_id}. Error: {str(e)}. Item attempted: {item_cleaned}")
        # Cognito requires the event to be returned, even on failure,
        # to not block user confirmation, unless you want to signal a hard stop.
        # For a post-confirmation, it's usually better to log and let Cognito proceed.
        # If this were a pre-token generation trigger, raising an error might be appropriate.

    return event