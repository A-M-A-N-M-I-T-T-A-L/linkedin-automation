import requests
import json
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from config.config import (
    LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, 
    OPENAI_MODEL, JOB_ANALYSIS_PROMPT, PROFILE_MATCHING_PROMPT
)
import logging

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self):
        self.llm = self._initialize_llm()
        
    def _initialize_llm(self):
        if LLM_PROVIDER == 'ollama':
            return Ollama(model=OLLAMA_MODEL)
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