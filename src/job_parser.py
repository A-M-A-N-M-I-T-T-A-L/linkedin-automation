from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from config.config import MAX_JOBS_TO_PARSE

logger = logging.getLogger(__name__)

class JobParser:
    def __init__(self, driver, llm_manager, db_manager):
        self.driver = driver
        self.llm_manager = llm_manager
        self.db_manager = db_manager
        self.jobs_parsed = 0
        
    def navigate_to_job_picks(self):
        try:
            self.driver.get("https://www.linkedin.com/jobs/")
            time.sleep(3)
            
            # Click on "Top job picks for you"
            top_picks = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Top job picks for you')]"))
            )
            top_picks.click()
            
            # Click "Show all"
            show_all = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Show all')]"))
            )
            show_all.click()
            
        except Exception as e:
            logger.error(f"Error navigating to job picks: {str(e)}")
            
    def parse_job_cards(self):
        while self.jobs_parsed < MAX_JOBS_TO_PARSE:
            try:
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
                
                for card in job_cards:
                    if self.jobs_parsed >= MAX_JOBS_TO_PARSE:
                        break
                        
                    job_data = self._extract_job_data(card)
                    if job_data:
                        # Analyze job with LLM
                        analysis = self.llm_manager.analyze_job(job_data['description'])
                        if analysis:
                            job_data.update(analysis)
                            self.db_manager.store_job(job_data, None)  # Add embedding logic
                            self.jobs_parsed += 1
                
                if not self._scroll_to_next_page():
                    break
                    
            except Exception as e:
                logger.error(f"Error parsing job cards: {str(e)}")
                break
                
    def _extract_job_data(self, card):
        try:
            return {
                'job_id': card.get_attribute('data-job-id'),
                'title': card.find_element(By.CLASS_NAME, "job-card-list__title").text,
                'company': card.find_element(By.CLASS_NAME, "job-card-container__company-name").text,
                'location': card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text,
                'description': self._get_job_description(card)
            }
        except Exception as e:
            logger.error(f"Error extracting job data: {str(e)}")
            return None
            
    def _get_job_description(self, card):
        try:
            card.click()
            time.sleep(2)
            description = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-description"))
            )
            return description.text
        except Exception as e:
            logger.error(f"Error getting job description: {str(e)}")
            return ""
            
    def _scroll_to_next_page(self):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error scrolling to next page: {str(e)}")
            return False 