import sys
import os
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.models.auth import User, Role, RoleType
from app.core.config import get_settings

def create_superuser(email: str, password: str):
    """Create a superuser account."""
    settings = get_settings()
    engine = create_engine(str(settings.DATABASE_URL))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if superuser already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists")
            return

        # Get superuser role
        superuser_role = db.query(Role).filter(Role.role == 'superuser').first()
        if not superuser_role:
            print("Superuser role not found. Please run migrations first.")
            return

        # Create superuser
        superuser = User(
            email=email,
            password_hash=get_password_hash(password),
            is_active=True,
            roles=[superuser_role]
        )
        db.add(superuser)
        db.commit()
        print(f"Superuser {email} created successfully")

    except Exception as e:
        print(f"Error creating superuser: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_superuser.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    create_superuser(email, password) 