from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class Resume:
    id: str
    user_id: str
    version: int
    content: Dict
    created_at: datetime
    last_modified: datetime
    file_path: Optional[str] = None
    format: str = "PDF"
    is_optimized: bool = False
    target_job_id: Optional[str] = None
    analysis: Optional[Dict] = None
    
    @property
    def skills(self) -> List[str]:
        return self.content.get('skills', [])
    
    @property
    def experience_years(self) -> float:
        experiences = self.content.get('experience', [])
        total_years = sum(exp.get('duration_years', 0) for exp in experiences)
        return round(total_years, 1)
    
    @property
    def latest_company(self) -> Optional[str]:
        experiences = self.content.get('experience', [])
        return experiences[0].get('company') if experiences else None