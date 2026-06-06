import asyncio
import time
from telegram import Update
from telegram.ext import ContextTypes
from utils import ForwardingStats, format_time
from config import FORWARDING_STATS, FORWARDING_COMPLETE
from keyboards import get_forwarding_keyboard
from database import db

class AutoForwarder:
    def __init__(self):
        self.active_forwards = {}
    
    async def start_forward(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                           source_chat_id, destination_chat_id, total_messages=100):
        """start auto forwarding process"""
        user_id = update.effective_user.id
        stats = ForwardingStats()
        self.active_forwards[user_id] = stats
        
        # send initial message
        message = await up
