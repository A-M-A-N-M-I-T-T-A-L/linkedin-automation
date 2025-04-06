from langchain_ollama import OllamaLLM
from langchain_community.chat_models import ChatOpenAI
from config.config import (
    LLM_PROVIDER, 
    OLLAMA_MODEL, 
    OPENAI_API_KEY, 
    OPENAI_MODEL,
    JOB_ANALYSIS_PROMPT,
    PROFILE_MATCHING_PROMPT,
    RESUME_ANALYSIS_PROMPT,
    RESUME_GENERATION_PROMPT
)
import json
import logging

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self):
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        if LLM_PROVIDER == 'ollama':
            return OllamaLLM(model=OLLAMA_MODEL)
        else:
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model_name=OPENAI_MODEL
            )
    
    def analyze_job(self, job_description):
        try:
            response = self.llm.predict(
                JOB_ANALYSIS_PROMPT + "\n" + job_description
            )
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error analyzing job: {str(e)}")
            return None
    
    def match_profile(self, job_requirements, profile_info):
        try:
            prompt = f"{PROFILE_MATCHING_PROMPT}\nJob: {json.dumps(job_requirements)}\nProfile: {json.dumps(profile_info)}"
            response = self.llm.predict(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error matching profile: {str(e)}")
            return None

    def analyze_resume_job_match(self, resume_text, job_details):
        try:
            prompt = f"{RESUME_ANALYSIS_PROMPT}\nResume: {resume_text}\nJob: {json.dumps(job_details)}"
            response = self.llm.predict(prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            return None

    def generate_optimized_resume(self, original_resume, job_details):
        try:
            prompt = f"{RESUME_GENERATION_PROMPT}\nOriginal Resume: {original_resume}\nJob: {json.dumps(job_details)}"
            response = self.llm.predict(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating resume: {str(e)}")
            return None