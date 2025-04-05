import time
from datetime import datetime
from .linkedin_bot import LinkedInBot
from config.config import MAX_CONNECTIONS_PER_DAY, CONNECTION_MESSAGE

class ConnectionManager:
    def __init__(self, linkedin_bot):
        self.bot = linkedin_bot
        self.connections_sent = 0
        self.last_reset = datetime.now().date()
        
    def reset_daily_count(self):
        current_date = datetime.now().date()
        if current_date > self.last_reset:
            self.connections_sent = 0
            self.last_reset = current_date
            
    def can_send_more_connections(self):
        self.reset_daily_count()
        return self.connections_sent < MAX_CONNECTIONS_PER_DAY
    
    def send_connection_request(self, name):
        if self.can_send_more_connections():
            if self.bot.send_connection_request(name, CONNECTION_MESSAGE):
                self.connections_sent += 1
                return True
        return False 