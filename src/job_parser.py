from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
        self.job_filters = {
            'min_experience': 0,
            'excluded_companies': set(),
            'required_skills': set(),
            'job_types': set()
        }
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 3)
        
    def set_filters(self, filters):
        self.job_filters.update(filters)
        
    def navigate_to_job_picks(self):
        try:
            self.driver.get("https://www.linkedin.com/jobs/")
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-home-tab"))
            )
            
            # Click on "Top job picks for you"
            top_picks = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Top job picks for you')]"))
            )
            top_picks.click()
            
            # Click "Show all"
            show_all = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show all')]"))
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
                        analysis = self.llm_manager.analyze_job(job_data['description'])
                        if analysis and self._meets_criteria(job_data, analysis):
                            job_data.update(analysis)
                            self.db_manager.store_job(job_data, None)
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
            description = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-description"))
            )
            # Wait for content to load
            self.short_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-description__content"))
            )
            return description.text
        except Exception as e:
            logger.error(f"Error getting job description: {str(e)}")
            return ""
            
    def _scroll_to_next_page(self):
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            self.short_wait.until(lambda driver: 
                driver.execute_script("return document.body.scrollHeight") > last_height
            )
            return True
        except Exception as e:
            logger.error(f"Error scrolling to next page: {str(e)}")
            return False

    def _meets_criteria(self, job_data, analysis):
        if not analysis:
            return False

        # Check minimum experience
        if analysis.get('years_of_experience', 0) < self.job_filters['min_experience']:
            return False

        # Check excluded companies
        if job_data['company'] in self.job_filters['excluded_companies']:
            return False

        # Check required skills
        if self.job_filters['required_skills']:
            job_skills = set(analysis.get('required_skills', []))
            if not self.job_filters['required_skills'].intersection(job_skills):
                return False

        # Check job type
        if self.job_filters['job_types']:
            if analysis.get('job_type') not in self.job_filters['job_types']:
                return False

        return True