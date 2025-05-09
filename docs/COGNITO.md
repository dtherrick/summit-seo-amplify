# AWS Cognito Configuration

This document provides details about the AWS Cognito User Pool configuration for the Summit SEO Amplify project.

## User Pool Configuration

- **User Pool ID**: us-east-1_amWoKMkcF
- **User Pool Name**: SummitSEOAmplifyUserPool
- **App Client ID**: 4s0peq2cv7vuuvq00frkrt13hb
- **App Client Name**: SummitSEOAmplifyWebClient
- **Cognito Domain**: https://summit-seo-amplify-dev.auth.us-east-1.amazoncognito.com

## Authentication Settings

- **Sign-in method**: Email
- **Password policy**: 
  - Minimum length: 8 characters
  - Requires uppercase letters
  - Requires lowercase letters
  - Requires numbers
  - Requires special characters
- **MFA**: Disabled (optional for future enhancement)
- **Email verification**: Enabled, automatically sent during sign-up

## Custom Attributes

Prefix `custom:` is automatically added to all custom attributes by Cognito.

| Attribute Name | Description | Type | Required | Mutable |
|----------------|-------------|------|----------|---------|
| tenant_id | Links users to their business/organization | String | No | Yes |
| subscription_tier | Tracks subscription level (free, basic, premium) | String | No | Yes |
| business_name | Name of the user's business | String | No | Yes |
| business_website | Primary website URL for SEO analysis | String | No | Yes |
| business_industry | Business industry for targeted recommendations | String | No | Yes |
| user_type | Defines user role (user, admin) | String | No | Yes |

## App Client Configuration

- **Client secret**: None (not required for browser-based applications)
- **Authentication flows**:
  - ALLOW_USER_SRP_AUTH (Secure Remote Password)
  - ALLOW_REFRESH_TOKEN_AUTH
  - ALLOW_USER_PASSWORD_AUTH
- **OAuth flows**:
  - Authorization code grant
  - Implicit grant
- **OAuth scopes**:
  - email
  - openid
  - profile
- **Callback URLs**:
  - http://localhost:5173/ (development)
  - https://summit-seo-amplify.example.com/ (production)

## Environment Variables

The following environment variables need to be set in the application:

```
# AWS Configuration
AWS_REGION=us-east-1

# Cognito Configuration
COGNITO_USER_POOL_ID=us-east-1_amWoKMkcF
COGNITO_APP_CLIENT_ID=4s0peq2cv7vuuvq00frkrt13hb
COGNITO_DOMAIN=summit-seo-amplify-dev
```

## Authentication Flow

1. User signs up with email and password
2. Cognito sends a verification code to the user's email
3. User verifies their email by entering the code
4. User can now sign in with their email and password
5. Upon successful authentication, Cognito issues JWT tokens:
   - ID token: Contains user information
   - Access token: For API authorization
   - Refresh token: For obtaining new ID and access tokens

## Using Cognito in the Application

### Backend (FastAPI)

1. JWT tokens from Cognito are verified on the backend using Cognito's JWKS
2. User information is extracted from verified tokens
3. Authorization is handled based on user attributes (e.g., user_type)

### Frontend (React)

1. Authentication UI can be implemented using:
   - Amplify Auth library
   - Cognito Hosted UI
   - Custom UI components
2. Tokens are stored securely in browser storage
3. Token refresh is handled automatically by Amplify or custom logic

## Deployment Considerations

1. For production, update the callback URLs with the actual domain
2. Consider enabling MFA for enhanced security
3. Configure SES for production email sending if needed (instead of Cognito default)
4. Review and adjust token expiration periods based on security requirements 