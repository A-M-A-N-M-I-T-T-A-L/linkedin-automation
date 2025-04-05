from fake_useragent import UserAgent
import random
from config.config import PROXY_LIST
import logging

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self):
        self.proxies = PROXY_LIST
        self.current_proxy = None
        self.user_agent = UserAgent()
        
    def get_proxy(self):
        if not self.proxies:
            return None
        self.current_proxy = random.choice(self.proxies)
        return {
            'http': self.current_proxy,
            'https': self.current_proxy
        }
    
    def get_headers(self):
        return {
            'User-Agent': self.user_agent.random
        }
    
    def rotate_proxy(self):
        previous = self.current_proxy
        while self.current_proxy == previous and len(self.proxies) > 1:
            self.current_proxy = random.choice(self.proxies)
        logger.info(f"Rotated proxy from {previous} to {self.current_proxy}") 