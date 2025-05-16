"""Test data factories for generating test data.

This module provides factory classes for creating test data instances
using factory_boy. These factories help maintain consistent test data
and make it easy to create related objects.

Example:
    ```python
    # Create a test business
    business = BusinessFactory()
    
    # Create a user associated with the business
    user = UserFactory(business=business)
    
    # Create a survey response for the business
    survey = SurveyResponseFactory(business=business)
    ```
"""

import factory
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, Business
from app.models.survey import SurveyResponse
from app.core.security import get_password_hash

class AsyncSQLAlchemyFactory(factory.Factory):
    """Base factory for SQLAlchemy models with async session support."""
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override to handle async session."""
        session = kwargs.pop('session', None)
        if not session or not isinstance(session, AsyncSession):
            raise ValueError("AsyncSession instance required")
            
        obj = model_class(*args, **kwargs)
        session.add(obj)
        return obj

class BusinessFactory(AsyncSQLAlchemyFactory):
    """Factory for creating test Business instances."""
    
    class Meta:
        model = Business
    
    id = factory.LazyFunction(uuid4)
    name = factory.Sequence(lambda n: f"Test Business {n}")
    description = factory.Faker('company_catch_phrase')
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

class UserFactory(AsyncSQLAlchemyFactory):
    """Factory for creating test User instances."""
    
    class Meta:
        model = User
    
    id = factory.LazyFunction(uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = factory.LazyFunction(
        lambda: get_password_hash("testpass123")
    )
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_superuser = False
    business = factory.SubFactory(BusinessFactory)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        """Add roles to the user after creation."""
        if not create:
            return
            
        if extracted:
            for role in extracted:
                self.roles.append(role)

class SuperUserFactory(UserFactory):
    """Factory for creating test superuser instances."""
    
    is_superuser = True
    business = None

class SurveyResponseFactory(AsyncSQLAlchemyFactory):
    """Factory for creating test SurveyResponse instances."""
    
    class Meta:
        model = SurveyResponse
    
    id = factory.LazyFunction(uuid4)
    customer_id = factory.LazyFunction(uuid4)
    business = factory.SubFactory(BusinessFactory)
    responses = factory.Dict({
        'satisfaction': factory.RandomInteger(min=1, max=5),
        'recommendation_likelihood': factory.RandomInteger(min=0, max=10),
        'feedback': factory.Faker('text', max_nb_chars=200),
        'areas_for_improvement': factory.List([
            factory.Faker('word') for _ in range(2)
        ])
    })
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc)) 