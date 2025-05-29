from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status
from datetime import datetime, timezone
from typing import Dict, Any

from ...utils.security import get_current_user
from ...models.user import User # Assuming User model is compatible with get_current_user output
from ...models.survey import SurveySubmissionPayload, SurveySubmissionResponse
# from backend.app.services.onboarding_service import OnboardingService # To be created
from ...core.config import settings # If needed for things like table names
from ...db.dynamodb import tenants_table # Import tenants_table directly
from botocore.exceptions import ClientError

router = APIRouter()

@router.post(
    "/survey",
    response_model=SurveySubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Onboarding Survey Data",
    description="Receives and processes the user's onboarding survey information. Requires authentication.",
)
async def submit_onboarding_survey(
    payload: SurveySubmissionPayload = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    # onboarding_service: OnboardingService = Depends(OnboardingService) # For DI of service layer
):
    """
    Endpoint to submit onboarding survey data.
    Requires authentication. The user context (e.g., user_id, tenant_id) will be
    extracted from the authenticated user details.

    For now, it will just log the received data and return a success message.
    Actual data persistence to a new DynamoDB table for survey results will be implemented later.
    """
    tenant_id = current_user.get("tenant_id")
    user_id = current_user.get("user_id") # Assuming 'user_id' is available
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant ID not found for user."
        )
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID not found for user."
        )

    try:
        # tenants_table is now imported directly
        # survey_data_dict = payload.dict(exclude_none=True) # Pydantic v1
        survey_data_dict = payload.model_dump(exclude_none=True) # Pydantic v2

        tenants_table.update_item(
            Key={'id': tenant_id},
            UpdateExpression="SET survey_data = :survey_data, updated_at = :updated_at",
            ExpressionAttributeValues={
                ':survey_data': survey_data_dict,
                ':updated_at': datetime.now(timezone.utc).isoformat() # Use timezone aware UTC timestamp
            }
        )

        print(f"Survey data successfully saved for tenant_id: {tenant_id}")
        # print(f"Payload: {payload.model_dump_json(indent=2)}") # Pydantic v2
        print(f"Payload: {payload.json(indent=2)}") # Pydantic v1 style

        return SurveySubmissionResponse(
            message="Survey data submitted successfully.",
            tenant_id=tenant_id,
            user_id=user_id, # Include user_id in the response
            submitted_at=datetime.now(timezone.utc).isoformat()
        )
    except ClientError as e:
        # Log the error details
        print(f"Error updating DynamoDB: {e.response['Error']['Message']}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not submit survey: {e.response['Error']['Message']}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

# TODO: Create OnboardingService in backend/app/services/onboarding_service.py
# This service would handle the business logic of validating and saving survey data.