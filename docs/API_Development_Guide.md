# API Development Guide: Summit SEO Amplify

## 1. Introduction

This guide provides best practices and conventions for developing APIs within the Summit SEO Amplify project. Our backend stack primarily consists of Python with FastAPI, running on AWS Lambda, fronted by Amazon API Gateway, and using Amazon Cognito for authentication. Adhering to these guidelines will help ensure consistency, security, and maintainability of our APIs.

## 2. Key Principles

*   **Security First:** Authentication and authorization are paramount. All endpoints must be appropriately secured.
*   **Clear Contracts:** Use Pydantic models for rigorous request and response validation and clear API contracts.
*   **Tenant Isolation:** All data operations and API responses must strictly enforce tenant boundaries.
*   **Asynchronous Operations:** Leverage FastAPI's async capabilities for I/O-bound operations and integrate with SQS/Step Functions for long-running background tasks.
*   **Comprehensive Logging & Error Handling:** Implement structured logging and consistent error responses.
*   **Testability:** Write unit and integration tests for API endpoints and business logic.

## 3. Development Workflow

1.  **Define Requirements:** Clearly understand the API's purpose, inputs, outputs, and authorization requirements.
2.  **Model Data (Pydantic):**
    *   Create Pydantic models for request bodies, query parameters, and response payloads.
    *   Place these in `backend/app/models/`.
3.  **Create Endpoint (FastAPI Router):**
    *   Add a new route in the appropriate router file within `backend/app/api/endpoints/`.
    *   Use dependency injection for common functionalities like authentication (`get_current_active_user`).
4.  **Implement Business Logic (Services):**
    *   Encapsulate core logic in service functions within `backend/app/services/` (if complex) or directly in the endpoint for simpler cases.
    *   Services should handle interactions with the database and other internal/external services.
5.  **Database Interaction:**
    *   Use the utility functions and pre-configured table objects from `backend/app/db/dynamodb.py`.
    *   Ensure all database queries correctly filter by `tenant_id`.
6.  **Authentication & Authorization:**
    *   Secure endpoints using the `Depends(get_current_active_user)` pattern.
    *   Extract `user_id` and `tenant_id` from the `current_user` object.
7.  **Error Handling:**
    *   Use `fastapi.HTTPException` for standard HTTP errors.
    *   Implement custom exception handling where necessary.
8.  **Testing:**
    *   Write unit tests for service logic.
    *   Write integration tests for API endpoints using FastAPI's `TestClient`.

## 4. Authentication & Authorization (Cognito)

*   **Securing Endpoints:** Most private endpoints are secured using the `CurrentUser = Depends(get_current_active_user)` dependency (defined in `backend/app/api/deps.py`). This function:
    *   Retrieves the JWT from the `Authorization` header.
    *   Verifies the token using `backend/app/utils/cognito.py`.
    *   Returns a `UserInDB` Pydantic model (or similar) containing user information, including `user_id` (from `sub` claim) and custom attributes like `custom:tenant_id`.
*   **JWT Claims:**
    *   `sub`: The unique identifier for the user (maps to `user_id`).
    *   `email`: User's email.
    *   `cognito:username`: Typically the same as `sub`.
    *   `aud`: Audience claim. For ID tokens, this should match your Cognito App Client ID.
    *   `custom:tenant_id`: Our custom attribute storing the tenant ID.
*   **Common Pitfall (`aud` vs. `client_id`):**
    *   When verifying ID tokens, the Cognito App Client ID is typically found in the `aud` claim. The `verify_cognito_token` utility in `backend/app/utils/cognito.py` should check `claims['aud']`. Misinterpreting this (e.g., looking for `client_id` directly in the claims of an ID token) will lead to authentication failures.
*   **Tenant ID Handling:**
    *   The `tenant_id` is crucial for data isolation. It should be extracted from the authenticated user's claims (e.g., `current_user.tenant_id` after being populated from `custom:tenant_id`).
    *   If `tenant_id` is missing from a user's JWT or DB record, this indicates an issue with the user provisioning process (e.g., Cognito post-confirmation trigger) and should be investigated. Endpoints relying on `tenant_id` should handle its absence gracefully, typically by returning a 403 Forbidden if the operation cannot proceed without it.

## 5. Data Validation & Serialization (Pydantic)

*   **Request Models:** Define Pydantic models for request bodies. FastAPI uses these to automatically validate incoming data.
    ```python
    # backend/app/models/survey.py
    from pydantic import BaseModel, HttpUrl
    from typing import List, Optional

    class SurveySubmission(BaseModel):
        industry: Optional[str] = None
        target_audience: Optional[str] = None
        # ... other fields
    ```
*   **Response Models:** Define Pydantic models for API responses using `response_model` in path operation decorators. This ensures the response conforms to the defined schema and helps with serialization.
    ```python
    # backend/app/api/endpoints/users.py
    from backend.app.models import User
    @router.get("/me", response_model=User)
    async def read_users_me(current_user: CurrentUser):
        # ... logic ...
        return current_user # FastAPI handles serialization based on User model
    ```
*   **Common Pitfall (`ResponseValidationError`):**
    *   A `fastapi.exceptions.ResponseValidationError` (often leading to a 500 Internal Server Error) occurs if the data returned by your endpoint does not match the `response_model`.
    *   **Cause:** Mismatch between fields in your Pydantic model and the actual data object (e.g., missing fields, incorrect data types, different field names like `user_id` in DB vs. `id` in model).
    *   **Solution:**
        1.  Inspect Lambda logs on CloudWatch to see the detailed validation error.
        2.  Ensure data transformation logic correctly maps database fields to your Pydantic model fields.
        3.  Verify that all required fields in the Pydantic model are present in the data being returned. If a field is optional in the data, mark it as `Optional` in the Pydantic model.
*   **Data Transformation:** It's common to fetch data from DynamoDB with one set of field names and need to transform it to match API response models.
    ```python
    # Example: Transforming a DynamoDB item to a Pydantic model
    db_item = {"user_id": "some-uuid", "email_address": "user@example.com", "name": "Test User"}
    api_user = User(id=db_item.get("user_id"), email=db_item.get("email_address"), full_name=db_item.get("name"))
    return api_user
    ```

## 6. Database Interaction (DynamoDB)

*   **Table Objects:** Use the pre-instantiated `users_table` and `tenants_table` from `backend/app/db/dynamodb.py`.
*   **Tenant Isolation:** CRITICAL: Every DynamoDB query or operation that accesses tenant-specific data MUST include a condition or filter based on `tenant_id`. This is the primary mechanism for data isolation.
*   **Data Consistency:** Ensure data integrity. For instance, the Cognito post-confirmation trigger is responsible for creating user records with a `tenant_id`. If this process fails or is incomplete, downstream API operations may fail.

## 7. API Gateway Configuration (via CDK)

*   **CDK Stack:** API Gateway (HTTP API) is defined in `infrastructure/lib/infrastructure-stack.ts`.
*   **CORS (Cross-Origin Resource Sharing):**
    *   CORS is configured in the CDK stack. Pay close attention to `allowOrigins`, `allowMethods`, `allowHeaders`.
    *   **Common Pitfall (Trailing Slashes / Exact Match):** The `allowOrigins` list must contain an *exact* match for the `Origin` header sent by the browser. A common mistake is a mismatch due to a trailing slash (e.g., `https://domain.com/` vs. `https://domain.com`).
    *   **Troubleshooting CORS:**
        1.  Use browser developer tools (Network tab) to inspect the preflight `OPTIONS` request and its response. Look for missing or incorrect `Access-Control-Allow-Origin` headers.
        2.  Double-check your API Gateway CORS configuration in the AWS console or CDK code.
        3.  Clear browser cache after making changes to CORS configuration.
*   **Lambda Integration:** API Gateway routes requests to the appropriate Lambda function(s) (defined in `infrastructure-stack.ts`).
*   **Path & Query Parameters:** FastAPI handles extraction of path and query parameters based on your endpoint definitions.

## 8. Error Handling & Logging

*   **Standard HTTP Errors:** Raise `fastapi.HTTPException(status_code=..., detail=...)` for typical error conditions.
    ```python
    from fastapi import HTTPException
    if not item_found:
        raise HTTPException(status_code=404, detail="Item not found")
    ```
*   **Custom Exceptions:** For domain-specific errors, you can define custom exceptions and use FastAPI exception handlers.
*   **Logging:**
    *   Use standard Python `logging` module or AWS Lambda Powertools for Python for structured logging.
    *   Log important events, errors, and relevant context (e.g., `user_id`, `tenant_id` for requests).
    *   **CloudWatch Logs are Essential:** All Lambda output (including logs and uncaught exceptions) goes to CloudWatch Logs. This is the primary place to debug API issues.

## 9. Troubleshooting Common API Issues

*   **401 Unauthorized:**
    *   **Check:** Is the `Authorization` header present with a valid Bearer token?
    *   **Check:** Decode the JWT (e.g., using jwt.io) to inspect its claims (`exp`, `aud`, `iss`).
    *   **Check:** Verify `backend/app/utils/cognito.py` correctly validates the `aud` claim against `COGNITO_APP_CLIENT_ID`.
    *   **Check:** Ensure the `COGNITO_USER_POOL_ID` and `COGNITO_APP_CLIENT_ID` environment variables in your Lambda function are correctly set.
*   **403 Forbidden:**
    *   **Check:** Authentication was successful, but the user lacks permission for the specific resource or action.
    *   **Check:** Internal logic in your endpoint. For example, is it trying to access data for a `tenant_id` that doesn't match the user's `tenant_id`? Is a required identifier like `tenant_id` missing from the `current_user` object?
    *   **CloudWatch Logs:** Look for specific log messages or conditions within your endpoint that might lead to a 403.
*   **500 Internal Server Error:**
    *   **Primary Action:** **Check CloudWatch Logs for the Lambda function.** This will almost always contain the detailed traceback.
    *   **Common Cause (FastAPI):** `fastapi.exceptions.ResponseValidationError` if the data returned doesn't match the `response_model`.
    *   **Common Cause:** Unhandled exceptions in your code (database errors, external service failures, bugs).
*   **CORS Errors (in browser console):**
    *   **Check:** API Gateway CORS configuration for `allowOrigins`, `allowMethods`, `allowHeaders`.
    *   **Check:** Ensure the requesting origin exactly matches one in `allowOrigins`.
    *   **Action:** Clear browser cache and retry.

## 10. Testing APIs

*   **Unit Tests:** Test business logic in services and utility functions independently.
*   **Integration Tests:** Use `fastapi.TestClient` to make requests to your API endpoints in a testing environment.
    *   Mock dependencies like database calls or external services where appropriate.
    *   Test successful scenarios, error conditions, and authorization.
    ```python
    # backend/app/tests/api/endpoints/test_users.py
    from fastapi.testclient import TestClient
    from backend.app.main import app # Your FastAPI app instance

    client = TestClient(app)

    def test_read_users_me_unauthenticated():
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401 # Or 403 depending on FastAPI version/setup

    def test_read_users_me_authenticated(mock_get_current_active_user): # Example with mocking auth
        # mock_get_current_active_user should return a valid user object
        app.dependency_overrides[get_current_active_user] = lambda: mock_get_current_active_user
        response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer faketoken"})
        assert response.status_code == 200
        assert response.json()["email"] == mock_get_current_active_user.email
        app.dependency_overrides = {} # Clear overrides
    ```

## 11. Deployment

*   **Infrastructure (API Gateway, Lambda, DynamoDB):** Deployed via AWS CDK (`infrastructure/lib/infrastructure-stack.ts`).
*   **Application Code:** Packaged and deployed to Lambda, typically automated via CI/CD (e.g., GitHub Actions that run `cdk deploy`).

This guide should serve as a living document. Please update it as our practices evolve or new patterns emerge. 