from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Job:
    id: str
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    experience_years: Optional[int]
    job_type: str
    created_at: datetime
    analysis: Optional[dict] = None
