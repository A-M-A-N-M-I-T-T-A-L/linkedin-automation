from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import random
import logging

logger = logging.getLogger(__name__)

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        self.session_start = None
        self.session_duration = 3600  # 1 hour
        self.notification_selectors = {
            'inbox': "//button[contains(@aria-label, 'Dismiss')]",
            'cookie': "//button[contains(@action-type, 'ACCEPT')]",
            'signup': "//button[contains(@data-control-name, 'dismiss')]"
        }
        self.wait = None
        self.short_wait = None
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 3)
        
    def login(self):
        self.driver.get('https://www.linkedin.com/login')
        
        # Enter email
        email_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)
        
        # Enter password
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        
        # Click login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for login to complete
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "feed-identity-module"))
        )
        self.session_start = time.time()
        self._dismiss_notifications()
        
    def _dismiss_notifications(self):
        for selector in self.notification_selectors.values():
            try:
                notification = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                notification.click()
                time.sleep(1)
            except TimeoutException:
                continue
        
    def _check_session(self):
        if not self.session_start or (time.time() - self.session_start) > self.session_duration:
            logger.info("Session expired, refreshing login")
            self.login()
        
    def search_jobs(self, keyword, location):
        self.driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}')
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results"))
        )
        
    def send_connection_request(self, name, custom_message=None):
        try:
            self._check_session()
            
            connect_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Connect']"))
            )
            
            if not connect_button.is_enabled():
                logger.warning(f"Connect button not enabled for {name}")
                return False
                
            connect_button.click()
            
            if custom_message:
                # Click 'Add a note' button
                add_note_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add a note']"))
                )
                add_note_button.click()
                
                # Wait for message field and enter text
                message_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "custom-message"))
                )
                message_field.clear()
                message_field.send_keys(custom_message.format(name=name))
            
            # Send connection request
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send now']"))
            )
            send_button.click()
            
            # Wait for confirmation
            self.short_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-toast-item--success"))
            )
            
            return True
            
        except StaleElementReferenceException:
            logger.error("Element became stale, refreshing page")
            self.driver.refresh()
            return self.send_connection_request(name, custom_message)
            
        except TimeoutException as e:
            logger.error(f"Timeout while sending connection request to {name}: {str(e)}")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error sending connection request to {name}: {str(e)}")
            return False

    def check_connection_status(self, profile_id):
        try:
            self._check_session()
            self.driver.get(f"https://www.linkedin.com/in/{profile_id}")
            time.sleep(2)

            # Check connection status
            connect_btn = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Connect']")
            pending_btn = self.driver.find_elements(By.CSS_SELECTOR, "[aria-label='Pending']")
            connected_btn = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Message']")

            if pending_btn:
                return "PENDING"
            elif connected_btn:
                return "ACCEPTED"
            elif connect_btn:
                return "NOT_CONNECTED"
            else:
                return "UNKNOWN"

        except Exception as e:
            logger.error(f"Error checking connection status: {str(e)}")
            return "ERROR"