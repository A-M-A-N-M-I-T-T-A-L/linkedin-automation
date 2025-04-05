from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=options)
        
    def login(self):
        self.driver.get('https://www.linkedin.com/login')
        
        # Enter email
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)
        
        # Enter password
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        
        # Click login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(5)  # Wait for login to complete
        
    def search_jobs(self, keyword, location):
        self.driver.get(f'https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}')
        time.sleep(3)
        
    def send_connection_request(self, name, custom_message=None):
        try:
            # Find and click connect button
            connect_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Connect']"))
            )
            connect_button.click()
            
            if custom_message:
                # Click 'Add a note' button
                add_note_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Add a note']"))
                )
                add_note_button.click()
                
                # Enter custom message
                message_field = self.driver.find_element(By.ID, "custom-message")
                message_field.send_keys(custom_message.format(name=name))
            
            # Send connection request
            send_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send now']")
            send_button.click()
            
            return True
            
        except TimeoutException:
            return False 