import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Define the Users table
    const usersTable = new dynamodb.Table(this, 'UsersTable', {
      tableName: 'SummitSEOAmplify-Users',
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
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
