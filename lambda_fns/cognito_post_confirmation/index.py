import boto3
import os
import uuid
from datetime import datetime, timezone

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
# Table name from environment variable. CDK will set this.
USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME', 'SummitSEOAmplify-Users')
TENANTS_TABLE_NAME = os.environ.get('TENANTS_TABLE_NAME', 'SummitSEOAmplify-Tenants') # Assuming you have an env var for tenants table
# It's good practice to ensure critical env vars are present
if not USERS_TABLE_NAME:
    raise EnvironmentError("Missing USERS_TABLE_NAME environment variable")
users_table = dynamodb.Table(USERS_TABLE_NAME)
tenants_table = dynamodb.Table(TENANTS_TABLE_NAME)

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
    timestamp = datetime.now(timezone.utc).isoformat()

    item = {
        'user_id': user_id,
        'cognito_id': cognito_id,
        'email': email,
        'full_name': user_attributes.get('name', user_attributes.get('preferred_username')),
        'created_at': timestamp,
        'updated_at': timestamp,
        'is_active': True,
        'last_login': timestamp,
        'profile_picture_url': user_attributes.get('picture'),
        'tenant_id': user_attributes.get('custom:tenant_id'),
        'subscription_tier': user_attributes.get('custom:subscription_tier', 'free'),
        'user_type': user_attributes.get('custom:user_type', 'user'),
        'business_name': user_attributes.get('custom:business_name'),
        'business_website': user_attributes.get('custom:business_website'),
        'business_industry': user_attributes.get('custom:business_industry'),
        'settings': {
            'notifications_enabled': True,
            'default_country_code': 'US',
        },
    }

    # Remove any keys with None values to avoid DynamoDB validation errors for empty strings
    item_cleaned = {k: v for k, v in item.items() if v is not None}

    try:
        users_table.put_item(Item=item_cleaned)
        print(f"Successfully created user profile for cognito_id: {cognito_id}, user_id: {user_id}. Item: {item_cleaned}")

        # If tenant_id and business_name were provided, create/update the Tenant record
        if item['tenant_id'] and item['business_name']:
            tenant_item = {
                'id': item['tenant_id'], # PK for Tenants table
                'name': item['business_name'],
                'owner_id': user_id, # Link to the user who created/owns this tenant
                'primary_website': item['business_website'],
                'business_email': email, # Or a separate collected business email
                'created_at': timestamp,
                'updated_at': timestamp,
                'is_active': True,
                'subscription_tier': item['subscription_tier'],
                'max_competitor_sites': 5, # Example default
                'max_projects_per_site': 3, # Example default
                'max_keywords_per_project': 100, # Example default
                'current_competitor_sites_count': 0,
                'current_projects_count': 0,
                'settings': item['settings'],
            }
            tenant_item_cleaned = {k: v for k, v in tenant_item.items() if v is not None}
            tenants_table.put_item(Item=tenant_item_cleaned)
            print(f"Successfully created/updated tenant {item['tenant_id']} for owner {user_id} in Tenants table.")
        else:
            print("Skipping tenant creation as custom:tenant_id or custom:business_name was not provided in user attributes.")

    except Exception as e:
        print(f"Error processing post confirmation for user {cognito_id}: {str(e)}")
        # Optionally, re-raise the exception if you want the Lambda to fail and potentially retry
        # raise e
        # Or handle specific errors, e.g., if you need to prevent Cognito from confirming the user
        # if the DB write fails critically. For now, we'll let Cognito confirm the user
        # and log the error. The user would exist in Cognito but might be in an inconsistent state in our DB.

    return event