from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='secrets.env')  # Specify the path to your env file

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
DB_PATH = "./local_chroma_store"

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = "logs/linkedin_automation.log"

# Dashboard Settings
DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', 8501))
DASHBOARD_HOST = os.getenv('DASHBOARD_HOST', 'localhost')
DASHBOARD_THEME = os.getenv('DASHBOARD_THEME', 'light')

# Data Storage
DATA_DIR = "data"
CONNECTIONS_DB = os.path.join(DATA_DIR, "connections.db")
VECTOR_DB = os.path.join(DATA_DIR, "vectors")
RESUME_DATA = os.path.join(DATA_DIR, "resume.json")

# Resume Optimization
MIN_SKILL_MATCH_PERCENTAGE = float(os.getenv('MIN_SKILL_MATCH', 70.0))
EXPERIENCE_MATCH_THRESHOLD = float(os.getenv('EXPERIENCE_MATCH_THRESHOLD', 2.0))

# Resume Settings
RESUME_TEMPLATE = os.path.join('templates', 'resume_template.html')
ALLOWED_RESUME_TYPES = ['pdf', 'docx']
MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5MB

# Resume Analysis Prompt
RESUME_ANALYSIS_PROMPT = """
Analyze the resume against the job requirements and provide:
1. Match percentage
2. Missing skills
3. Experience alignment
4. Specific improvement suggestions
Format the output as JSON.
"""

# Resume Generation Prompt
RESUME_GENERATION_PROMPT = """
Generate an optimized resume content that:
1. Highlights relevant experience
2. Uses job-specific keywords
3. Quantifies achievements
4. Matches required skills
Format the output as structured text.
"""

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

# Connection Message
CONNECTION_MESSAGE = os.getenv('CONNECTION_MESSAGE', "Hi [Name], I came across your profile and was impressed by your experience in [Field. I'd love to connect and learn more about your work.")

# Job Application Settings
MAX_APPLICATIONS_PER_DAY = int(os.getenv('MAX_APPLICATIONS_PER_DAY', 10))

# Search Settings
MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 50))
SEARCH_KEYWORDS = os.getenv('SEARCH_KEYWORDS', 'Software Engineer')
SEARCH_LOCATION = os.getenv('SEARCH_LOCATION', 'India')