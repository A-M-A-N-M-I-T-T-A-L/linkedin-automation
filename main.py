import os
from src.linkedin_bot import LinkedInBot
from src.connection_manager import ConnectionManager
from src.llm_manager import LLMManager
from src.db_manager import DBManager
from src.proxy_manager import ProxyManager
from src.job_parser import JobParser
from config.config import (
    LINKEDIN_EMAIL, LINKEDIN_PASSWORD, 
    MAX_JOBS_TO_PARSE, MAX_CONNECTIONS_PER_DAY
)

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# Apply limits to the bot
LinkedInBot.MAX_JOBS_TO_PARSE = MAX_JOBS_TO_PARSE
ConnectionManager.MAX_CONNECTIONS_PER_DAY = MAX_CONNECTIONS_PER_DAY

import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/linkedin_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    # Initialize components
    llm_manager = LLMManager()
    db_manager = DBManager()
    proxy_manager = ProxyManager()
    
    # Initialize the bot with proxy support
    bot = LinkedInBot(
        LINKEDIN_EMAIL, 
        LINKEDIN_PASSWORD,
        proxy_manager=proxy_manager
    )
    
    connection_manager = ConnectionManager(bot)
    
    try:
        # Setup and login
        bot.setup_driver()
        bot.login()
        
        # Initialize job parser
        job_parser = JobParser(bot.driver, llm_manager, db_manager)
        
        # Parse jobs
        logger.info("Starting job parsing...")
        job_parser.navigate_to_job_picks()
        job_parser.parse_job_cards()
        
        # Process connection requests
        logger.info("Processing connection requests...")
        connection_manager.process_pending_connections()
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        if bot.driver:
            bot.driver.quit()

if __name__ == "__main__":
    main()