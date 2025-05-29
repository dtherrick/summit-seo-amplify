from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status
from datetime import datetime, timezone
from typing import Dict, Any

from backend.app.utils.security import get_current_user
from backend.app.models.user import User # Assuming User model is compatible with get_current_user output
from backend.app.models.survey import SurveySubmissionPayload, SurveySubmissionResponse
from backend.app.services.onboarding_service import OnboardingService # To be created
from backend.app.core.config import settings # If needed for things like table names
from backend.app.db.dynamodb import get_dynamodb_table # Assuming this utility exists

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
    if not tenant_id:
        raise HTTPException(
            status_code=400,
            detail="User is not associated with a tenant. Cannot submit survey."
        )

    try:
        tenants_table = get_dynamodb_table(settings.TENANTS_TABLE_NAME)

        # Using .model_dump() for Pydantic v2, or .dict() for Pydantic v1
        # Assuming Pydantic v1 based on .json() later. If v2, use model_dump(exclude_none=True)
        survey_data_dict = payload.dict(exclude_none=True)

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
            # survey_id=survey_id # Example if you generate an ID after saving
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error processing survey for tenant {tenant_id}:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the survey."
        )

# TODO: Create OnboardingService in backend/app/services/onboarding_service.py
# This service would handle the business logic of validating and saving survey data.