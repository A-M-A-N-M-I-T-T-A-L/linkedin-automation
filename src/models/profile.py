from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Profile:
    id: str
    name: str
    headline: str
    company: str
    location: str
    connections_count: Optional[int] = None
    shared_connections: Optional[List[str]] = None
    experience: Optional[List[dict]] = None
    education: Optional[List[dict]] = None
    skills: Optional[List[str]] = None
    is_employee: bool = False
    seniority_level: Optional[str] = None
    created_at: datetime = datetime.now()
    last_updated: datetime = datetime.now()