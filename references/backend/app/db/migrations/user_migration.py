"""Migration script for transitioning to FastAPI Users."""
from typing import List, Tuple
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Role, User

async def migrate_roles(session: AsyncSession) -> List[Tuple[str, UUID]]:
    """Migrate roles from the old system to the new one."""
    # Create default roles
    default_roles = [
        Role(name="superuser", description="Super administrator with full access"),
        Role(name="business_admin", description="Business administrator"),
        Role(name="business_user", description="Regular business user"),
    ]
    
    # Add roles to session
    for role in default_roles:
        session.add(role)
    
    await session.commit()
    
    # Return role name to ID mapping
    return [(role.name, role.id) for role in default_roles]

async def migrate_users(
    session: AsyncSession,
    role_mapping: List[Tuple[str, UUID]],
) -> None:
    """Migrate users from the old system to the new one.
    
    This function should be called after creating the new tables but before
    dropping the old ones. It will:
    1. Read users from the old tables
    2. Create new user records with the same data
    3. Migrate role assignments
    4. Migrate business relationships
    """
    # Get old users
    result = await session.execute(
        select(User).where(User.__table__.name == "users_old")
    )
    old_users = result.scalars().all()
    
    # Create role mapping dict
    role_dict = dict(role_mapping)
    
    # Migrate each user
    for old_user in old_users:
        # Create new user with the same data
        new_user = User(
            id=old_user.id,
            email=old_user.email,
            hashed_password=old_user.password_hash,
            is_active=old_user.is_active,
            is_verified=True,  # Assume existing users are verified
            business_id=old_user.business_id,
            has_completed_survey=old_user.has_completed_survey,
        )
        
        # Map old roles to new roles
        for old_role in old_user.roles:
            if old_role.role in role_dict:
                role_result = await session.execute(
                    select(Role).where(Role.id == role_dict[old_role.role])
                )
                new_role = role_result.scalar_one()
                new_user.roles.append(new_role)
        
        session.add(new_user)
    
    await session.commit()

async def cleanup_old_tables(session: AsyncSession) -> None:
    """Drop old user-related tables after successful migration."""
    # Drop old tables in the correct order
    await session.execute("DROP TABLE IF EXISTS sessions CASCADE")
    await session.execute("DROP TABLE IF EXISTS user_roles_old CASCADE")
    await session.execute("DROP TABLE IF EXISTS roles_old CASCADE")
    await session.execute("DROP TABLE IF EXISTS users_old CASCADE")
    
    await session.commit()

async def run_migration(session: AsyncSession) -> None:
    """Run the complete migration process."""
    try:
        # Rename old tables
        await session.execute("ALTER TABLE users RENAME TO users_old")
        await session.execute("ALTER TABLE roles RENAME TO roles_old")
        await session.execute("ALTER TABLE user_roles RENAME TO user_roles_old")
        
        # Create new tables (should be done through Alembic)
        
        # Migrate roles and get mapping
        role_mapping = await migrate_roles(session)
        
        # Migrate users
        await migrate_users(session, role_mapping)
        
        # Cleanup old tables
        await cleanup_old_tables(session)
        
        await session.commit()
        
    except Exception as e:
        await session.rollback()
        raise Exception(f"Migration failed: {str(e)}") 