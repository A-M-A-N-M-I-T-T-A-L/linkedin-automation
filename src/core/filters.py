from dataclasses import dataclass
from typing import List, Optional, Set

@dataclass
class JobFilter:
    min_experience: int = 0
    required_skills: Optional[List[str]] = None
    job_types: Optional[List[str]] = None
    excluded_companies: Optional[Set[str]] = None
    location: Optional[str] = None
    salary_range: Optional[tuple[int, int]] = None
    remote_only: bool = False
    
    def to_dict(self):
        return {
            'min_experience': self.min_experience,
            'required_skills': self.required_skills,
            'job_types': self.job_types,
            'excluded_companies': list(self.excluded_companies) if self.excluded_companies else None,
            'location': self.location,
            'salary_range': self.salary_range,
            'remote_only': self.remote_only
        }