import time
from collections import deque
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, max_requests=60, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    def can_make_request(self):
        current_time = time.time()
        
        # Remove old requests
        while self.requests and current_time - self.requests[0] > self.time_window:
            self.requests.popleft()
            
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
            
        return False

    def wait_for_next_slot(self):
        while not self.can_make_request():
            time.sleep(1)
