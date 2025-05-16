from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from ...core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    SecurityUtils,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ...core.auth import get_current_user, get_current_active_superuser, RoleChecker
from ...db.session import get_db
from ...models.auth import User, Business, Role, RoleType
from ...schemas.auth import (
    Token,
    UserCreate,
    UserResponse,
    BusinessCreate,
    BusinessResponse,
    UserLogin
)

router = APIRouter()

@router.post("/business/signup", response_model=BusinessResponse)
async def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    """Create a new business account with an admin user."""
    # Generate customer ID
    customer_id = SecurityUtils.generate_customer_id(business.name)
    
    # Create business
    db_business = Business(
        name=business.name,
        customer_id=customer_id
    )
    db.add(db_business)
    db.flush()  # Flush to get the business ID
    
    # Create admin user
    admin_role = db.query(Role).filter(Role.role == RoleType.BUSINESS_ADMIN).first()
    if not admin_role:
        raise HTTPException(status_code=500, detail="Role configuration error")
    
    admin_user = User(
        email=business.admin_email,
        password_hash=get_password_hash(business.admin_password),
        business_id=db_business.id,
        roles=[admin_role]
    )
    db.add(admin_user)
    db.commit()
    
    return BusinessResponse(
        id=str(db_business.id),
        name=db_business.name,
        customer_id=db_business.customer_id
    )

@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(RoleChecker(["superuser", "business_admin"])),
    db: Session = Depends(get_db)
):
    """Create a new user (requires admin privileges)."""
    # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # For business admins, ensure they can only create users in their business
    if not any(role.role == "superuser" for role in current_user.roles):
        if current_user.business_id != user.business_id:
            raise HTTPException(status_code=403, detail="Cannot create user for other businesses")
    
    # Get the business user role
    business_user_role = db.query(Role).filter(Role.role == RoleType.BUSINESS_USER).first()
    if not business_user_role:
        raise HTTPException(status_code=500, detail="Role configuration error")
    
    # Create user
    db_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        business_id=user.business_id,
        roles=[business_user_role]
    )
    db.add(db_user)
    db.commit()
    
    return UserResponse(
        id=str(db_user.id),
        email=db_user.email,
        business_id=str(db_user.business_id)
    )

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        business_id=str(current_user.business_id),
        roles=[role.role for role in current_user.roles]
    )

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(RoleChecker(["superuser", "business_admin"])),
    db: Session = Depends(get_db)
):
    """List users (filtered by business for business admins)."""
    if any(role.role == "superuser" for role in current_user.roles):
        users = db.query(User).all()
    else:
        users = db.query(User).filter(User.business_id == current_user.business_id).all()
    
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            business_id=str(user.business_id)
        )
        for user in users
    ] 