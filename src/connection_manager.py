import time
from datetime import datetime
import logging
from .linkedin_bot import LinkedInBot
from config.config import MAX_CONNECTIONS_PER_DAY, CONNECTION_MESSAGE
from .rate_limiter import RateLimiter
from .retry_manager import RetryManager
from .connection_tracker import ConnectionTracker

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self, linkedin_bot):
        self.bot = linkedin_bot
        self.connections_sent = 0
        self.last_reset = datetime.now().date()
        self.rate_limiter = RateLimiter()
        self.retry_manager = RetryManager()
        self.connection_history = {}
        self.priority_queue = []
        self.connection_tracker = ConnectionTracker()
        self.validation_delay = 60  # seconds to wait before validating
        
    def reset_daily_count(self):
        current_date = datetime.now().date()
        if current_date > self.last_reset:
            self.connections_sent = 0
            self.last_reset = current_date
            
    def can_send_more_connections(self):
        self.reset_daily_count()
        return self.connections_sent < MAX_CONNECTIONS_PER_DAY
    
    @RetryManager.retry_with_backoff
    def send_connection_request(self, profile_data):
        if not self.can_send_more_connections():
            return False

        if self.connection_tracker.is_duplicate(profile_data['id']):
            logger.info(f"Skipping duplicate connection request to {profile_data['name']}")
            return False
            
        self.rate_limiter.wait_for_next_slot()
        
        success = self.bot.send_connection_request(
            profile_data['name'], 
            self._generate_custom_message(profile_data)
        )
        
        if success:
            self.connections_sent += 1
            self.connection_tracker.add_connection(
                profile_data['id'],
                profile_data['name'],
                profile_data.get('company', ''),
                profile_data.get('notes', '')
            )
            self._validate_connection_status(profile_data['id'])
            
        return success

    def _validate_connection_status(self, profile_id):
        time.sleep(self.validation_delay)
        status = self.bot.check_connection_status(profile_id)
        self.connection_tracker.update_status(profile_id, status)
        return status == "ACCEPTED"
        
    def prioritize_connections(self, profiles):
        scored_profiles = []
        for profile in profiles:
            score = self._calculate_priority_score(profile)
            scored_profiles.append((score, profile))
        
        self.priority_queue = sorted(scored_profiles, reverse=True)
        
    def _calculate_priority_score(self, profile):
        score = 0
        if profile.get('is_employee', False):
            score += 10
        if profile.get('shared_connections', 0) > 10:
            score += 5
        if profile.get('seniority_level', '').lower() in ['senior', 'manager', 'director']:
            score += 8
        return score
        
    def _generate_custom_message(self, profile):
        template = """Hi {name},
        I noticed you work at {company} and I'm very interested in the {role} position. 
        Would you be open to a brief chat about your experience there?
        Best regards"""
        
        return template.format(
            name=profile['name'],
            company=profile['company'],
            role=profile['target_role']
        )