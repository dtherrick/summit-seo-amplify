# Database Design

This document outlines the design of the DynamoDB tables used in the Summit SEO Amplify project.

## Guiding Principles

- **Single Table Design (per entity for now):** While not strictly single-table design across the entire application, each core entity (Users, Tenants) has its own table for clarity in this phase.
- **On-Demand Billing:** Tables use `PAY_PER_REQUEST` billing mode for cost-effectiveness during development and for workloads that are not easily predictable.
- **Clear Primary Keys:** Each table uses a simple `id` (string) as its partition key.
- **Global Secondary Indexes (GSIs):** GSIs are created to support common query patterns not covered by the primary key.
- **TTL for relevant data:** The `Users` table has a `ttl` attribute for potential future use with DynamoDB Time To Live.
- **Removal Policy (Development):** Tables are set with a `DESTROY` removal policy for development, meaning they will be deleted if the CloudFormation stack is destroyed. This should be changed to `RETAIN` or `SNAPSHOT` for production.

## Tables

### 1. Users Table

- **Table Name:** `SummitSEOAmplify-Users`
- **Purpose:** Stores user profile information.
- **Partition Key:** `id` (String) - Unique identifier for the user.
- **Billing Mode:** On-Demand (`PAY_PER_REQUEST`)
- **Time To Live (TTL) Attribute:** `ttl` (Number) - Unix timestamp.

#### Global Secondary Indexes (GSIs)

1.  **`CognitoIdIndex`**
    *   **Partition Key:** `cognito_id` (String) - The user's unique ID from Cognito.
    *   **Projection:** All attributes (`ALL`)
    *   **Purpose:** Allows fetching a user record directly using their Cognito ID, which is useful after authentication.

#### Key Attributes (derived from `backend/app/models/user.py`)

| Attribute           | Type                | Description                                     | Notes                                     |
|---------------------|---------------------|-------------------------------------------------|-------------------------------------------|
| `id`                | String (UUID)       | Primary key, unique user identifier.            | Partition Key                             |
| `cognito_id`        | String              | User's unique identifier from AWS Cognito.      | GSI Partition Key (`CognitoIdIndex`)      |
| `tenant_id`         | String (UUID)       | Identifier of the tenant the user belongs to.   |                                           |
| `email`             | String (Email)      | User's email address.                           |                                           |
| `full_name`         | String (Optional)   | User's full name.                               |                                           |
| `is_active`         | Boolean             | Whether the user account is active.             | Defaults to `true`.                       |
| `user_type`         | String              | Role of the user (e.g., "user", "admin").       | Defaults to `"user"`.                     |
| `subscription_tier` | String              | User's subscription level (e.g., "free", "basic"). | Defaults to `"free"`.                     |
| `created_at`        | String (ISO 8601)   | Timestamp of user creation.                     | Stored as ISO 8601 string (DynamoDB best practice) |
| `updated_at`        | String (ISO 8601, Optional) | Timestamp of last update.               | Stored as ISO 8601 string                 |
| `ttl`               | Number (Optional)   | TTL timestamp for item expiration.              |                                           |

### 2. Tenants Table

- **Table Name:** `SummitSEOAmplify-Tenants`
- **Purpose:** Stores information about tenant organizations/businesses.
- **Partition Key:** `id` (String) - Unique identifier for the tenant.
- **Billing Mode:** On-Demand (`PAY_PER_REQUEST`)

#### Global Secondary Indexes (GSIs)

1.  **`OwnerIdIndex`**
    *   **Partition Key:** `owner_id` (String) - The `id` of the user who owns/created the tenant.
    *   **Projection:** All attributes (`ALL`)
    *   **Purpose:** Allows fetching all tenants associated with a specific user (owner).

#### Key Attributes (derived from `backend/app/models/tenant.py`)

| Attribute             | Type                | Description                                         | Notes                                     |
|-----------------------|---------------------|-----------------------------------------------------|-------------------------------------------|
| `id`                  | String (UUID)       | Primary key, unique tenant identifier.              | Partition Key                             |
| `owner_id`            | String (UUID)       | `id` of the user who owns this tenant.              | GSI Partition Key (`OwnerIdIndex`)        |
| `name`                | String              | Name of the tenant/business.                        |                                           |
| `business_email`      | String (Email)      | Official email address for the business.            |                                           |
| `primary_website`     | String (URL, Optional) | Primary website URL of the business.             |                                           |
| `industry`            | String (Optional)   | Industry the business operates in.                  |                                           |
| `description`         | String (Optional)   | A brief description of the tenant/business.         |                                           |
| `is_active`           | Boolean             | Whether the tenant account is active.               | Defaults to `true`.                       |
| `subscription_tier`   | String              | Tenant's subscription level (e.g., "free", "basic").| Defaults to `"free"`.                     |
| `max_competitor_sites`| Number              | Max number of competitor sites allowed for analysis.| Defaults to `5` (for free tier).          |
| `created_at`          | String (ISO 8601)   | Timestamp of tenant creation.                       | Stored as ISO 8601 string                 |
| `updated_at`          | String (ISO 8601, Optional) | Timestamp of last update.                 | Stored as ISO 8601 string                 |

## Future Considerations

- **Stream Processing:** DynamoDB Streams could be enabled for tasks like data replication to other services (e.g., OpenSearch for analytics), triggering notifications, or creating audit logs.
- **Fine-grained Access Control:** While GSIs help, more complex queries might necessitate evolving the data model or using additional query capabilities.
- **Data Archival:** For very large datasets, consider strategies for archiving older data to S3 via DynamoDB export or Data Pipelines. 