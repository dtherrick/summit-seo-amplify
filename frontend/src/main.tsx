import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import outputs from "../../amplify_outputs.json";
import { Amplify } from "aws-amplify";
import { parseAmplifyConfig } from "aws-amplify/utils";

// Log the raw outputs to see what's being loaded
console.log(
  "Raw amplify_outputs.json loaded:",
  JSON.stringify(outputs, null, 2)
);

// Parse the imported outputs
const baseConfig = parseAmplifyConfig(outputs);

// Extract the specific API configuration from the imported outputs
const apiPlugin = outputs.api?.plugins?.awsAPIPlugin;
const apiDetails = apiPlugin ? apiPlugin["SummitSEOAmplifyAPI"] : undefined;

let apiConfig = {};
if (apiDetails) {
  apiConfig = {
    SummitSEOAmplifyAPI: {
      endpoint: apiDetails.endpoint,
      region: apiDetails.region,
      authorizationType: apiDetails.authorizationType,
    },
  };
}

// Configure Amplify, merging the Auth config from outputs and explicitly setting API.REST
Amplify.configure({
  ...baseConfig,
  API: {
    ...baseConfig.API,
    REST: {
      ...(baseConfig.API?.REST || {}),
      ...apiConfig,
    },
  },
});

console.log(
  "Amplify.getConfig() after Amplify.configure(outputs):",
  JSON.stringify(Amplify.getConfig(), null, 2)
);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
