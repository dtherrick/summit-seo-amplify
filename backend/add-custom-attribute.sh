#!/bin/bash

USER_POOL_ID="us-east-1_amWoKMkcF"

# Add tenant_id attribute
echo "Adding tenant_id attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "tenant_id",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

# Add subscription_tier attribute
echo "Adding subscription_tier attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "subscription_tier",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

# Add business_name attribute
echo "Adding business_name attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "business_name",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

# Add business_website attribute
echo "Adding business_website attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "business_website",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

# Add business_industry attribute
echo "Adding business_industry attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "business_industry",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

# Add user_type attribute
echo "Adding user_type attribute..."
aws cognito-idp add-custom-attributes \
  --user-pool-id $USER_POOL_ID \
  --custom-attributes \
  '[{
    "Name": "user_type",
    "AttributeDataType": "String",
    "DeveloperOnlyAttribute": false,
    "Mutable": true,
    "Required": false,
    "StringAttributeConstraints": {
      "MinLength": "0",
      "MaxLength": "2048"
    }
  }]'

echo "All custom attributes added successfully!"