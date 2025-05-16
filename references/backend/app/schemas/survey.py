from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum

class Categories(str, Enum):
    FASHION = "Fashion"
    TECHNOLOGY = "Technology"
    HEALTH_WELLNESS = "Health & Wellness"
    FOOD_BEVERAGE = "Food & Beverage"
    TRAVEL = "Travel"
    HOME_GARDEN = "Home & Garden"
    EDUCATION = "Education"
    FINANCE = "Finance"
    ENTERTAINMENT = "Entertainment"
    AUTOMOTIVE = "Automotive"

class GeneralInformation(BaseModel):
    brand_name: str = Field(..., description="The name of your brand")
    brand_description: Optional[str] = Field(None, description="A short description of your brand")
    url: HttpUrl = Field(..., description="The URL of your brand")
    categories: Optional[List[Categories]] = Field(None, description="The categories of your brand")

class Audience(BaseModel):
    who_is_your_audience: Optional[str] = Field(None, description="Description of your target audience")
    needs_and_preferences: Optional[str] = Field(None, description="Audience needs and preferences")

class PillarKeywords(BaseModel):
    informational_intent: Optional[str] = Field(None, description="Keywords for information-seeking customers")
    commercial_intent: Optional[str] = Field(None, description="Keywords for customers ready to buy")
    transactional_intent: Optional[str] = Field(None, description="Keywords for customers ready to buy from you")
    brand_intent: Optional[str] = Field(None, description="Keywords related to your brand")

class SEO(BaseModel):
    seed_keywords: Optional[str] = Field(None, description="Initial keywords for content generation")
    pillar_keywords: Optional[PillarKeywords] = Field(None, description="Keywords organized by intent")

class Competitors(BaseModel):
    key_competitors: Optional[str] = Field(None, description="Main competitors in your market")
    secondary_competitors: Optional[str] = Field(None, description="Secondary competitors")

class SurveyData(BaseModel):
    general_information: GeneralInformation
    audience: Optional[Audience] = Field(None, description="Information about your target audience")
    seo: Optional[SEO] = Field(None, description="SEO and keyword information")
    competitors: Optional[Competitors] = Field(None, description="Competitor information")
    guardrails: Optional[str] = Field(None, description="Topics or areas to avoid in content")
    content_pillars: Optional[str] = Field(None, description="Key themes for content generation")

class SurveyResponseCreate(BaseModel):
    """Schema for creating a new survey response."""
    customer_id: str = Field(..., description="Unique identifier for the customer")
    response_data: SurveyData = Field(..., description="The survey response data")

class SurveyResponseDB(SurveyResponseCreate):
    """Schema for survey response as stored in the database."""
    id: int = Field(..., description="Unique identifier for the survey response")
    created_at: datetime = Field(..., description="Timestamp when the response was created")
    updated_at: datetime = Field(..., description="Timestamp when the response was last updated")

    class Config:
        from_attributes = True

# Move the example response before SurveyResponseCreate
example_survey_response = {
    "customer_id": "customer123",
    "response_data": {
        "general_information": {
            "brand_name": "Example Brand",
            "brand_description": "A great brand description",
            "url": "https://example.com",
            "categories": ["Technology", "Education"]
        },
        "audience": {
            "who_is_your_audience": "Tech-savvy professionals",
            "needs_and_preferences": "Looking for innovative solutions"
        },
        "seo": {
            "seed_keywords": "innovation, technology, education",
            "pillar_keywords": {
                "informational_intent": "how to learn programming",
                "commercial_intent": "best programming courses",
                "transactional_intent": "buy programming course",
                "brand_intent": "example brand courses"
            }
        },
        "competitors": {
            "key_competitors": "Competitor A, Competitor B",
            "secondary_competitors": "Secondary A, Secondary B"
        },
        "guardrails": "No content about specific pricing",
        "content_pillars": "Innovation, Education, Technology"
    }
} 