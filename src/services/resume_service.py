from src.resume_generator import ResumeGenerator
from src.llm_manager import LLMManager
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ResumeService:
    def __init__(self, generator: ResumeGenerator, llm_manager: LLMManager):
        self.generator = generator
        self.llm_manager = llm_manager

    def analyze_resume(self, resume_text: str, job_details: Dict):
        return self.llm_manager.analyze_resume_job_match(resume_text, job_details)

    def generate_optimized_resume(self, resume_text: str, job_details: Dict):
        analysis = self.analyze_resume(resume_text, job_details)
        return self.generator.generate(resume_text, job_details, analysis)