from dotenv import load_dotenv
import os

load_dotenv()

# LinkedIn Credentials
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# LLM Settings
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')  # 'ollama' or 'openai'
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

# Limits
MAX_CONNECTIONS_PER_DAY = int(os.getenv('MAX_CONNECTIONS_PER_DAY', 20))
MAX_JOBS_TO_PARSE = int(os.getenv('MAX_JOBS_TO_PARSE', 100))
MAX_REQUESTS_PER_COMPANY = int(os.getenv('MAX_REQUESTS_PER_COMPANY', 5))

# Proxy Settings
USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
PROXY_LIST = os.getenv('PROXY_LIST', '').split(',')

# Database
DB_PATH = "data/vectors"

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = "logs/linkedin_automation.log"

# LLM Instructions for job analysis
JOB_ANALYSIS_PROMPT = """
Analyze the following job posting and extract:
1. Required skills
2. Years of experience
3. Key responsibilities
4. Company culture indicators
5. Potential matching criteria for referrals
Format the output as JSON.
"""

PROFILE_MATCHING_PROMPT = """
Given the job requirements and the profile information:
1. Calculate match percentage
2. Identify key matching points
3. Suggest personalized connection message
4. Flag if this is a high-potential match
Format the output as JSON.
""" 