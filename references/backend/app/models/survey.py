from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional

from app.core.database import Base

# Association table for many-to-many relationship between goals and survey responses
survey_goals = Table(
    'survey_goals',
    Base.metadata,
    Column('survey_id', Integer, ForeignKey('survey_responses.id'), primary_key=True),
    Column('goal_id', Integer, ForeignKey('goals.id'), primary_key=True)
)

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to survey responses
    survey_responses = relationship("SurveyResponse", secondary=survey_goals, back_populates="goals")

class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True, nullable=False)
    response_data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to goals
    goals = relationship("Goal", secondary=survey_goals, back_populates="survey_responses") 