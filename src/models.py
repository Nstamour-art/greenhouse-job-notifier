from pydantic import BaseModel
from typing import Optional
from datetime import date

class Job(BaseModel):
    greenhouse_id: int
    internal_id: int
    title: str
    department: Optional[str]
    location: str
    content: str
    url: str
    date_updated: date

class UserProfile(BaseModel):
    id: int
    name: str

class MatchedJob(BaseModel):
    job: Job
    relevance_score: float
    llm_explanation: Optional[str]

class JobMatchResult(BaseModel):
    relevance_score: float
    explanation: str