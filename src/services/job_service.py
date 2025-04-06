from src.job_parser import JobParser
from src.llm_manager import LLMManager
from src.db_manager import DBManager
from src.models.job import Job
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class JobService:
    def __init__(self, linkedin_bot, llm_manager: LLMManager, db_manager: DBManager):
        self.job_parser = JobParser(linkedin_bot.driver, llm_manager, db_manager)
        self.llm_manager = llm_manager
        self.db_manager = db_manager

    def parse_jobs(self, filters: Dict = None) -> List[Job]:
        if filters:
            self.job_parser.set_filters(filters)
        return self.job_parser.parse_job_cards()

    def analyze_job(self, job_id: str) -> Dict:
        job = self.db_manager.get_job(job_id)
        if not job:
            return None
        return self.llm_manager.analyze_job(job.description)

    def get_job_recommendations(self, skills: List[str]) -> List[Job]:
        return self.db_manager.query_similar_jobs(skills)
