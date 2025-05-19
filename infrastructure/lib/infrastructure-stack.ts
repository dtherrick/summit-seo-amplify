import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as path from 'path';
import { HttpApi, CorsHttpMethod, HttpNoneAuthorizer, HttpMethod } from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpUserPoolAuthorizer } from 'aws-cdk-lib/aws-apigatewayv2-authorizers';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
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
      runtime: lambda.Runtime.PYTHON_3_12, // Or your preferred Python version
      handler: 'app.main.handler', // Corrected handler path
      code: lambda.Code.fromAsset(path.join(__dirname, '../../backend'), { // Asset path
        bundling: {
          image: lambda.Runtime.PYTHON_3_12.bundlingImage, // Use stock Python bundling image
          command: [
            'bash', '-c', [
              'pip install -r requirements.txt -t /asset-output', // Install to staging dir
              'cp -au . /asset-output' // Copy the rest of the code
            ].join(' && ')
          ],
        },
      }),
      role: apiLambdaRole,
      environment: {
        USERS_TABLE_NAME: usersTable.tableName,
        TENANTS_TABLE_NAME: tenantsTable.tableName,
        // Add other necessary environment variables
      },
      timeout: cdk.Duration.seconds(30),
    });

    // 1. Get your frontend's App Client ID (the one that generates the JWTs you're sending)
    const frontendAppClientId = '4s0peq2cv7vuuvq00frkrt13hb';

    // 2. Import this existing User Pool Client into your CDK app
    const importedUserPoolClient = cognito.UserPoolClient.fromUserPoolClientId(
        this,
        'ImportedFrontendClient', // Logical ID for this imported client in CDK
        frontendAppClientId
    );

    // Define Cognito Authorizer for API Gateway, now using the imported client
    const authorizer = new HttpUserPoolAuthorizer('CognitoAuthorizer', userPool, {
      userPoolClients: [importedUserPoolClient], // Use the imported client object
    });

    // Define the HTTP API Gateway
    const httpApi = new HttpApi(this, 'SummitSEOAmplifyHttpApi', {
      apiName: 'SummitSEOAmplifyApi',
      description: 'API for Summit SEO Amplify',
      corsPreflight: {
        allowHeaders: ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token'],
        allowMethods: [
          CorsHttpMethod.OPTIONS,
          CorsHttpMethod.GET,
          CorsHttpMethod.POST,
          CorsHttpMethod.PUT,
          CorsHttpMethod.PATCH,
          CorsHttpMethod.DELETE,
        ],
        allowCredentials: true,
        allowOrigins: ['http://localhost:3000', 'https://main.d9e32iiq5ru07.amplifyapp.com'], // Replace with your frontend URLs
      },
      defaultAuthorizer: authorizer, // Secure all routes by default
    });

    // Create Lambda integration
    const apiLambdaIntegration = new HttpLambdaIntegration('ApiLambdaIntegration', apiLambda);

    // Define routes for /users/me
    httpApi.addRoutes({
      path: '/api/v1/users/me',
      methods: [HttpMethod.GET, HttpMethod.PUT],
      integration: apiLambdaIntegration,
      // Authorizer is already set at the API level, so it applies here too.
    });

    // Add public route for /
    httpApi.addRoutes({
      path: '/',
      methods: [HttpMethod.GET],
      integration: apiLambdaIntegration,
      authorizer: new HttpNoneAuthorizer(), // Make this route public
    });

    // Add public route for /health
    httpApi.addRoutes({
      path: '/health',
      methods: [HttpMethod.GET],
      integration: apiLambdaIntegration,
      authorizer: new HttpNoneAuthorizer(), // Make this route public
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
