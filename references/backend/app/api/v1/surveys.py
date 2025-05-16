"""Survey response management router module.

This module provides API endpoints for managing survey responses in the application.
It handles CRUD operations for survey responses and includes schema validation
and example data endpoints.

The module provides:
- Survey response creation and retrieval
- Survey response updates
- Survey schema information
- Example survey data

API Endpoints:
- POST / - Create a new survey response
- GET / - List all survey responses (with pagination)
- GET /{customer_id} - Get a specific survey response
- PUT /{customer_id} - Update a survey response
- GET /schema/example - Get example survey data
- GET /schema/structure - Get survey schema definition

Example:
    ```python
    from fastapi import FastAPI
    from app.api.v1.surveys import router as survey_router

    app = FastAPI()
    app.include_router(survey_router, prefix="/api/v1/surveys")

    # Example usage with httpx client:
    async with httpx.AsyncClient() as client:
        # Create survey response
        response = await client.post(
            "http://localhost:8000/api/v1/surveys",
            json={
                "customer_id": "ACME-123",
                "response_data": {"question1": "answer1"}
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        survey = response.json()
    ```

Note:
    Survey responses are linked to customers and can only be submitted once
    per user. The response data schema is flexible and defined by the
    SurveyResponseCreate model.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.models.survey import SurveyResponse
from app.models.auth import User
from app.core.auth import get_current_user
from app.schemas.survey import SurveyResponseCreate, SurveyResponseDB, example_survey_response

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=SurveyResponseDB)
async def create_survey_response(
    survey: SurveyResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new survey response.

    This endpoint creates a new survey response and marks the user's survey
    as completed. The response data is validated against the survey schema.

    Args:
        survey: The survey response data
        db: Database session (injected by FastAPI)
        current_user: The authenticated user (injected by FastAPI)

    Returns:
        SurveyResponseDB: The created survey response

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 500 if database operation fails

    Example:
        ```python
        # With authenticated client
        response = await client.post(
            "/api/v1/surveys",
            json={
                "customer_id": "ACME-123",
                "response_data": {"question1": "answer1"}
            }
        )
        survey = response.json()
        ```

    Note:
        This endpoint performs a transaction that updates both the survey
        response and the user's survey completion status.
    """
    try:
        logger.debug(f"Received survey data for customer: {survey.customer_id}")
        
        # Convert the Pydantic model to a dict with JSON-serializable values
        response_data = survey.response_data.model_dump(mode='json')
        logger.debug(f"Converted response data: {response_data}")
        
        # Create the survey response object
        db_survey = SurveyResponse(
            customer_id=survey.customer_id,
            response_data=response_data
        )
        
        # Add and commit to database
        try:
            # Mark the user's survey as completed
            current_user.has_completed_survey = True
            
            db.add(db_survey)
            db.add(current_user)
            db.commit()
            db.refresh(db_survey)
            db.refresh(current_user)
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(db_error)}"
            )
            
        return db_survey
        
    except Exception as e:
        logger.error(f"Error in create_survey_response: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/{customer_id}", response_model=SurveyResponseDB)
def get_survey_response(customer_id: str, db: Session = Depends(get_db)):
    """Get a specific customer's survey response.

    This endpoint retrieves a survey response by customer ID.

    Args:
        customer_id: The ID of the customer
        db: Database session (injected by FastAPI)

    Returns:
        SurveyResponseDB: The survey response

    Raises:
        HTTPException: 404 if survey response is not found

    Example:
        ```python
        response = await client.get(f"/api/v1/surveys/ACME-123")
        survey = response.json()
        ```
    """
    survey = db.query(SurveyResponse).filter(
        SurveyResponse.customer_id == customer_id
    ).first()
    if survey is None:
        raise HTTPException(status_code=404, detail="Survey response not found")
    return survey

@router.get("/", response_model=List[SurveyResponseDB])
def list_survey_responses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all survey responses with pagination.

    This endpoint returns a paginated list of all survey responses.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        db: Database session (injected by FastAPI)

    Returns:
        List[SurveyResponseDB]: List of survey responses

    Example:
        ```python
        # Get second page of 50 responses
        response = await client.get("/api/v1/surveys?skip=50&limit=50")
        surveys = response.json()
        ```

    Note:
        Consider implementing cursor-based pagination for large datasets
        in production.
    """
    surveys = db.query(SurveyResponse).offset(skip).limit(limit).all()
    return surveys

@router.put("/{customer_id}", response_model=SurveyResponseDB)
def update_survey_response(
    customer_id: str,
    survey: SurveyResponseCreate,
    db: Session = Depends(get_db)
):
    """Update an existing survey response.

    This endpoint updates a survey response for a specific customer.

    Args:
        customer_id: The ID of the customer
        survey: The updated survey response data
        db: Database session (injected by FastAPI)

    Returns:
        SurveyResponseDB: The updated survey response

    Raises:
        HTTPException: 404 if survey response is not found

    Example:
        ```python
        response = await client.put(
            f"/api/v1/surveys/ACME-123",
            json={
                "customer_id": "ACME-123",
                "response_data": {"question1": "new_answer"}
            }
        )
        updated_survey = response.json()
        ```
    """
    db_survey = db.query(SurveyResponse).filter(
        SurveyResponse.customer_id == customer_id
    ).first()
    if db_survey is None:
        raise HTTPException(status_code=404, detail="Survey response not found")
    
    db_survey.response_data = survey.response_data.dict()
    db.commit()
    db.refresh(db_survey)
    return db_survey

@router.get("/schema/example")
def get_survey_example():
    """Get an example of a valid survey response.

    This endpoint returns an example survey response that demonstrates
    the expected format and data types.

    Returns:
        dict: Example survey response data

    Example:
        ```python
        response = await client.get("/api/v1/surveys/schema/example")
        example = response.json()
        ```
    """
    return example_survey_response

@router.get("/schema/structure")
def get_survey_schema():
    """Get the JSON schema for survey responses.

    This endpoint returns the JSON schema that defines the structure
    and validation rules for survey responses.

    Returns:
        dict: JSON schema for survey responses

    Example:
        ```python
        response = await client.get("/api/v1/surveys/schema/structure")
        schema = response.json()
        ```

    Note:
        Use this schema to validate survey responses on the client side
        before submission.
    """
    return SurveyResponseCreate.model_json_schema() 