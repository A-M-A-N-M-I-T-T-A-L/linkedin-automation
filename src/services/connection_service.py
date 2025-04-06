from src.linkedin_bot import LinkedInBot
from src.connection_tracker import ConnectionTracker
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ConnectionService:
    def __init__(self, bot: LinkedInBot, tracker: ConnectionTracker):
        self.bot = bot
        self.tracker = tracker

    def send_connection(self, profile_data: Dict):
        if self.tracker.is_duplicate(profile_data['id']):
            logger.info(f"Skipping duplicate connection request to {profile_data['name']}")
            return False

        success = self.bot.send_connection_request(profile_data['name'], profile_data.get('message'))
        if success:
            self.tracker.add_connection(
                profile_id=profile_data['id'],
                name=profile_data['name'],
                company=profile_data.get('company', ''),
                notes=profile_data.get('notes', '')
            )
        return success