import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as path from 'path';
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

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfrastructureQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
