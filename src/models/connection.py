from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Connection:
    profile_id: str
    name: str
    company: str
    status: str  # SENT, PENDING, ACCEPTED, REJECTED
    sent_date: datetime
    response_date: Optional[datetime] = None
    notes: Optional[str] = None
    custom_message: Optional[str] = None
    priority_score: Optional[float] = None