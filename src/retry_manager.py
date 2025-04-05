import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RetryManager:
    def __init__(self, max_retries=3, base_delay=1, max_delay=60):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def retry_with_backoff(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < self.max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retry_count += 1
                    if retry_count == self.max_retries:
                        logger.error(f"Max retries reached for {func.__name__}: {str(e)}")
                        raise
                    delay = min(self.base_delay * (2 ** retry_count), self.max_delay)
                    logger.warning(f"Retry {retry_count} for {func.__name__} after {delay}s")
                    time.sleep(delay)
            return None
        return wrapper
