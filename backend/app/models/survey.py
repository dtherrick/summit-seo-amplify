from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class GeneralInformationPayload(BaseModel):
    brand_name: Optional[str] = None
    brand_description: Optional[str] = None
    url: Optional[str] = None # Frontend sends without scheme, HttpUrl expects scheme
    categories: Optional[List[str]] = None
    products_services: Optional[str] = None
    location_info: Optional[str] = None
    niche: Optional[str] = None

class AudiencePayload(BaseModel):
    who_is_your_audience: Optional[str] = None
    needs_and_preferences: Optional[str] = None

class PillarKeywordsPayload(BaseModel):
    informational_intent: Optional[List[str]] = None
    commercial_intent: Optional[List[str]] = None
    transactional_intent: Optional[List[str]] = None
    brand_intent: Optional[List[str]] = None

class SeoPayload(BaseModel):
    seed_keywords: Optional[List[str]] = None
    pillar_keywords: Optional[PillarKeywordsPayload] = None

class CompetitorsContentPayload(BaseModel):
    key_competitors: Optional[List[str]] = None # Frontend sends without scheme
    secondary_competitors: Optional[List[str]] = None # Frontend sends without scheme

class GoalsPayload(BaseModel):
    primary_goals: Optional[List[str]] = None
    current_marketing_activities: Optional[List[str]] = None

class SurveySubmissionPayload(BaseModel):
    general_information: Optional[GeneralInformationPayload] = None
    audience: Optional[AudiencePayload] = None
    seo: Optional[SeoPayload] = None
    competitors_content: Optional[CompetitorsContentPayload] = None
    guardrails: Optional[str] = None
    content_pillars: Optional[str] = None
    brand_image_tone: Optional[str] = None
    goals: Optional[GoalsPayload] = None

class SurveySubmissionResponse(BaseModel):
    message: str
    survey_id: Optional[str] = None # Or some other identifier if you create a record
    # Potentially other fields like tenant_id if relevant here