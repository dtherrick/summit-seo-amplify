import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as path from 'path';
import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import { HttpUserPoolAuthorizer } from 'aws-cdk-lib/aws-apigatewayv2-authorizers';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define the Users table
    const usersTable = new dynamodb.Table(this, 'UsersTable', {
      tableName: 'SummitSEOAmplify-Users',
      partitionKey: { name: 'user_id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      timeToLiveAttribute: 'ttl',
    });

    // Add Global Secondary Index for Cognito ID
    usersTable.addGlobalSecondaryIndex({
      indexName: 'CognitoIdIndex',
      partitionKey: { name: 'cognito_id', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // Define the Tenants table
    const tenantsTable = new dynamodb.Table(this, 'TenantsTable', {
      tableName: 'SummitSEOAmplify-Tenants',
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Add Global Secondary Index for Owner ID
    tenantsTable.addGlobalSecondaryIndex({
      indexName: 'OwnerIdIndex',
      partitionKey: { name: 'owner_id', type: dynamodb.AttributeType.STRING },
      projectionType: dynamodb.ProjectionType.ALL,
    });

    // Import existing Cognito User Pool
    const userPoolId = 'us-east-1_amWoKMkcF'; // From docs/COGNITO.md
    const userPool = cognito.UserPool.fromUserPoolId(this, 'ImportedUserPool', userPoolId);

    // IAM Role for the Lambda function
    const postConfirmationLambdaRole = new iam.Role(this, 'PostConfirmationLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Grant PutItem permission to the Users table
    usersTable.grantWriteData(postConfirmationLambdaRole);
    // If you need to be more specific (least privilege):
    // postConfirmationLambdaRole.addToPolicy(new iam.PolicyStatement({
    //   actions: ['dynamodb:PutItem'],
    //   resources: [usersTable.tableArn],
    // }));

    // Define the Post-Confirmation Lambda function
    const postConfirmationLambda = new lambda.Function(this, 'PostConfirmationLambda', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../../lambda_fns/cognito_post_confirmation')),
      role: postConfirmationLambdaRole,
      environment: {
        USERS_TABLE_NAME: usersTable.tableName,
      },
      timeout: cdk.Duration.seconds(30), // Adjust timeout as needed
    });

    // REMOVED: userPool.addTrigger(cognito.UserPoolOperation.POST_CONFIRMATION, postConfirmationLambda);
    // You will need to manually configure this trigger in the AWS Cognito console
    // after deploying this stack. Point the Post-Confirmation trigger to the
    // 'postConfirmationLambda' function created above.

    // --- Start of API Lambda and API Gateway Resources ---

    // IAM Role for the API Lambda function
    const apiLambdaRole = new iam.Role(this, 'ApiLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
      ],
    });

    // Grant permissions to API Lambda to access DynamoDB tables (adjust as needed)
    usersTable.grantReadWriteData(apiLambdaRole);
    tenantsTable.grantReadWriteData(apiLambdaRole);

    // Define the API Lambda function (FastAPI backend)
    const apiLambda = new lambda.Function(this, 'ApiLambda', {
      runtime: lambda.Runtime.PYTHON_3_9, // Or your preferred Python version
      handler: 'main.handler', // Assuming Mangum adapter in main.py
      code: lambda.Code.fromAsset(path.join(__dirname, '../../backend')), // Path to your FastAPI app
      role: apiLambdaRole,
      environment: {
        USERS_TABLE_NAME: usersTable.tableName,
        TENANTS_TABLE_NAME: tenantsTable.tableName,
        // Add other necessary environment variables
      },
      timeout: cdk.Duration.seconds(30),
    });

    // Import existing Cognito User Pool (if not already defined above)
    // const userPoolId = 'us-east-1_amWoKMkcF'; // Ensure this is the correct ID
    // const userPool = cognito.UserPool.fromUserPoolId(this, 'ImportedUserPoolForApi', userPoolId);

    // Define Cognito Authorizer for API Gateway
    const authorizer = new HttpUserPoolAuthorizer('CognitoAuthorizer', userPool, {
      userPoolClients: [userPool.addClient('apiClient', {
        // Configure client as needed, e.g., OAuth flows if you plan to use them directly with API GW
        // For just token validation, defaults are often fine.
         authFlows: {
          userSrp: true,
        },
        oAuth: {
          flows: {
            authorizationCodeGrant: true,
            implicitCodeGrant: true, // Example: if you need id_token directly for some flows
          },
          scopes: [ cognito.OAuthScope.EMAIL, cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE ],
          // callbackUrls: ['https://myapp.com/callback'], // Replace with your actual callback URLs
          // logoutUrls: ['https://myapp.com/logout'],    // Replace with your actual logout URLs
        },
      })],
    });

    // Define the HTTP API Gateway
    const httpApi = new apigwv2.HttpApi(this, 'SummitSEOAmplifyHttpApi', {
      apiName: 'SummitSEOAmplifyApi',
      description: 'API for Summit SEO Amplify',
      corsPreflight: {
        allowHeaders: ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token'],
        allowMethods: [
          apigwv2.CorsHttpMethod.OPTIONS,
          apigwv2.CorsHttpMethod.GET,
          apigwv2.CorsHttpMethod.POST,
          apigwv2.CorsHttpMethod.PUT,
          apigwv2.CorsHttpMethod.PATCH,
          apigwv2.CorsHttpMethod.DELETE,
        ],
        allowCredentials: true,
        allowOrigins: ['http://localhost:3000', 'https://main.youramplifyapp.com'], // Replace with your frontend URLs
      },
      defaultAuthorizer: authorizer, // Secure all routes by default
    });

    // Create Lambda integration
    const apiLambdaIntegration = new HttpLambdaIntegration('ApiLambdaIntegration', apiLambda);

    // Define routes for /users/me
    httpApi.addRoutes({
      path: '/users/me',
      methods: [apigwv2.HttpMethod.GET, apigwv2.HttpMethod.PUT],
      integration: apiLambdaIntegration,
      // Authorizer is already set at the API level, so it applies here too.
    });

    // --- End of API Lambda and API Gateway Resources ---

    // --- End of New Lambda Resources ---

    // Output table names
    new cdk.CfnOutput(this, 'UsersTableNameOutput', {
      value: usersTable.tableName,
      description: 'Name of the Users DynamoDB table',
    });

    new cdk.CfnOutput(this, 'TenantsTableNameOutput', {
      value: tenantsTable.tableName,
      description: 'Name of the Tenants DynamoDB table',
    });

    // Output API Gateway URL
    new cdk.CfnOutput(this, 'ApiGatewayUrl', {
      value: httpApi.url!,
      description: 'URL of the API Gateway',
    });

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfrastructureQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
