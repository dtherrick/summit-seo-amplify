from fastapi import APIRouter, Depends, HTTPException
from typing import Any

# Mock Pydantic models (ideally these would be in a separate models file)
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True

class UserResponse(UserBase):
    user_id: str # Or Cognito sub
    tenant_id: str | None = None
    subscription_tier: str | None = None
    business_name: str | None = None
    business_website: str | None = None
    business_industry: str | None = None
    user_type: str = "user"

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    business_name: str | None = None
    business_website: str | None = None
    business_industry: str | None = None

router = APIRouter()

# Mock current user - in a real app, this would come from your auth dependency
MOCK_USER_ID = "mock-user-123"
MOCK_COGNITO_SUB = "abcdef12-3456-7890-abcd-ef1234567890"

async def get_current_user_mock():
    # In a real application, this dependency would:
    # 1. Extract the JWT token from the Authorization header.
    # 2. Validate the token (e.g., using python-jose with Cognito public keys).
    # 3. Extract user information (like 'sub' or 'username') from the token.
    # 4. Optionally, fetch user details from DynamoDB based on the 'sub'.
    # For now, it returns a mock cognito_sub.
    return {"sub": MOCK_COGNITO_SUB, "email": "testuser@example.com"} # Mock, replace with actual auth

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user_mock)) -> Any:
    """
    Get current user profile.
    """
    # In a real app, you'd fetch this from DynamoDB using current_user['sub']
    return UserResponse(
        user_id=current_user["sub"],
        email=current_user["email"],
        first_name="John",
        last_name="Doe",
        is_active=True,
        tenant_id="mock-tenant-id",
        subscription_tier="free",
        business_name="MockBiz",
        business_website="https://mock.biz",
        business_industry="Tech",
        user_type="user"
    )

@router.put("/me", response_model=UserResponse)
async def update_users_me(
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_user_mock)
) -> Any:
    """
    Update current user profile.
    """
    # In a real app, you would:
    # 1. Fetch the user from DynamoDB using current_user['sub'].
    # 2. Update the fields provided in user_in.
    # 3. Save the updated user back to DynamoDB.
    print(f"Updating user {current_user['sub']} with data: {user_in.model_dump(exclude_unset=True)}")
    # For now, just return a mock updated response
    return UserResponse(
        user_id=current_user['sub'],
        email=current_user['email'],
        first_name=user_in.first_name if user_in.first_name is not None else "John",
        last_name=user_in.last_name if user_in.last_name is not None else "Doe",
        is_active=True,
        tenant_id="mock-tenant-id",
        subscription_tier="free",
        business_name=user_in.business_name if user_in.business_name is not None else "MockBiz",
        business_website=user_in.business_website if user_in.business_website is not None else "https://mock.biz",
        business_industry=user_in.business_industry if user_in.business_industry is not None else "Tech",
        user_type="user"
    )