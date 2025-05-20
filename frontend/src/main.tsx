import React from "react";
import ReactDOM from "react-dom/client";
// import App from "./App.tsx"; // App.tsx will no longer be the main entry point
import "./index.css";
import outputs from "../../amplify_outputs.json";
import { Amplify } from "aws-amplify";
import { Authenticator } from '@aws-amplify/ui-react'; // Import Authenticator Provider
import '@aws-amplify/ui-react/styles.css';

import { RouterProvider, createRouter } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen'; // Import the generated route tree

// Log the raw outputs to see what's being loaded
// console.log(
//   "Raw amplify_outputs.json loaded:",
//   JSON.stringify(outputs, null, 2)
// );

// Create an Amplify configuration using the endpoint directly from outputs.json
// The endpoint in outputs.json is typically like: "https://[api-id].execute-api.[region].amazonaws.com/[stage]/"
const amplifyConfig = {
  Auth: {
    Cognito: {
      userPoolId: outputs.auth.user_pool_id,
      userPoolClientId: outputs.auth.user_pool_client_id,
      identityPoolId: outputs.auth.identity_pool_id
    }
  },
  API: {
    REST: {
      SummitSEOAmplifyAPI: { // This key must match the apiName used in get/put calls
        endpoint: outputs.api.plugins.awsAPIPlugin.SummitSEOAmplifyAPI.endpoint, // Use as is from outputs
        region: outputs.api.plugins.awsAPIPlugin.SummitSEOAmplifyAPI.region,
        authorization: {
          type: 'AMAZON_COGNITO_USER_POOLS' // Ensure this matches your API's auth type
        }
      }
    }
  }
};

// Configure Amplify with this direct configuration
Amplify.configure(amplifyConfig);

// Log the configuration to verify it's correct
// console.log(
//   "Amplify.getConfig() after custom configuration:",
//   JSON.stringify(Amplify.getConfig(), null, 2)
// );

// Create a new router instance
const router = createRouter({ routeTree });

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Authenticator.Provider> {/* Wrap RouterProvider with Authenticator.Provider */}
      <RouterProvider router={router} />
    </Authenticator.Provider>
  </React.StrictMode>
);
