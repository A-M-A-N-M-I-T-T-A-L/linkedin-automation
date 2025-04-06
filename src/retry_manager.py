import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class RetryManager:
    @staticmethod
    def retry_with_backoff(max_retries=3, backoff_factor=2):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retries = 0
                delay = 1  # Initial delay in seconds
                while retries < max_retries:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        retries += 1
                        logger.warning(
                            f"Retry {retries}/{max_retries} for {func.__name__} due to error: {e}"
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                logger.error(f"Failed after {max_retries} retries for {func.__name__}")
                raise
            return wrapper
        return decorator
