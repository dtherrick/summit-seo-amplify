chunk-NXESFFTV.js?v=02933c50:21609 Download the React DevTools for a better development experience: https://reactjs.org/link/react-devtools
main.tsx:10 Raw amplify_outputs.json loaded: {
  "auth": {
    "user_pool_id": "us-east-1_amWoKMkcF",
    "aws_region": "us-east-1",
    "user_pool_client_id": "4s0peq2cv7vuuvq00frkrt13hb",
    "identity_pool_id": "us-east-1:3cd3a356-552b-4177-898c-8696965f7bae",
    "mfa_methods": [],
    "standard_required_attributes": [
      "email"
    ],
    "username_attributes": [
      "email"
    ],
    "user_verification_types": [
      "email"
    ],
    "mfa_configuration": "NONE",
    "password_policy": {
      "min_length": 8,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "require_uppercase": true
    },
    "unauthenticated_identities_enabled": true
  },
  "api": {
    "plugins": {
      "awsAPIPlugin": {
        "SummitSEOAmplifyAPI": {
          "endpointType": "REST",
          "endpoint": "https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/",
          "region": "us-east-1",
          "authorizationType": "AMAZON_COGNITO_USER_POOLS"
        }
      }
    }
  },
  "version": "1.3"
}
main.tsx:45 Amplify.getConfig() after Amplify.configure(outputs): {
  "Auth": {
    "Cognito": {
      "userPoolId": "us-east-1_amWoKMkcF",
      "userPoolClientId": "4s0peq2cv7vuuvq00frkrt13hb",
      "identityPoolId": "us-east-1:3cd3a356-552b-4177-898c-8696965f7bae",
      "passwordFormat": {
        "requireLowercase": true,
        "requireNumbers": true,
        "requireUppercase": true,
        "requireSpecialCharacters": true,
        "minLength": 8
      },
      "mfa": {
        "status": "off",
        "smsEnabled": false,
        "totpEnabled": false
      },
      "allowGuestAccess": true,
      "loginWith": {
        "email": true,
        "phone": false,
        "username": false
      },
      "userAttributes": {
        "email": {
          "required": true
        }
      }
    }
  },
  "API": {
    "REST": {
      "SummitSEOAmplifyAPI": {
        "endpoint": "https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/",
        "region": "us-east-1",
        "authorizationType": "AMAZON_COGNITO_USER_POOLS"
      }
    }
  }
}
cognito-identity.us-east-1.amazonaws.com/:1 
            
            
           Failed to load resource: the server responded with a status of 400 ()
cognito-identity.us-east-1.amazonaws.com/:1 
            
            
           Failed to load resource: the server responded with a status of 400 ()
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
UserProfile.tsx:46 Error fetching user profile: NetworkError: A network error has occurred.
    at fetchTransferHandler (chunk-R2S6FG23.js?v=02933c50:6091:13)
    at async retryMiddleware (chunk-R2S6FG23.js?v=02933c50:5781:20)
    at async userAgentMiddleware (chunk-R2S6FG23.js?v=02933c50:6041:22)
    at async transferHandler (aws-amplify_api.js?v=02933c50:7430:16)
    at async job (aws-amplify_api.js?v=02933c50:7271:24)
    at async fetchProfile (UserProfile.tsx:34:26)
fetchProfile @ UserProfile.tsx:46
127.0.0.1/:1 Access to fetch at 'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me' from origin 'http://127.0.0.1:5173' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/users/me:1 
            
            
           Failed to load resource: net::ERR_FAILED
UserProfile.tsx:46 Error fetching user profile: NetworkError: A network error has occurred.
    at fetchTransferHandler (chunk-R2S6FG23.js?v=02933c50:6091:13)
    at async retryMiddleware (chunk-R2S6FG23.js?v=02933c50:5781:20)
    at async userAgentMiddleware (chunk-R2S6FG23.js?v=02933c50:6041:22)
    at async transferHandler (aws-amplify_api.js?v=02933c50:7430:16)
    at async job (aws-amplify_api.js?v=02933c50:7271:24)
    at async fetchProfile (UserProfile.tsx:34:26)
fetchProfile @ UserProfile.tsx:46
