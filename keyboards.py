from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

def get_main_keyboard():
    """main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("👨‍💻 developer", url=f"https://t.me/{DEVELOPER.replace('@', '')}"),
            InlineKeyboardButton("👥 support group", url=SUPPORT_GROUP)
        ],
        [
            InlineKeyboardButton("📢 support channel", url=SUPPORT_CHANNEL),
            InlineKeyboardButton("🎥 youtube", url=YOUTUBE_CHANNEL)
        ],
        [
            InlineKeyboardButton("❓ help", callback_data="help"),
            InlineKeyboardButton("ℹ️ about", callback_data="about")
        ],
        [
            InlineKeyboardButton("⚙️ settings", callback_data="settings"),
            InlineKeyboardButton("📊 stats", callback_data="stats")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_force_sub_keyboard():
    """force subscription keyboard"""
    keyboard = [
        [InlineKeyboardButton("📢 join channel", url=FORCE_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ joined", callback_data="check_joined")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_forwarding_keyboard():
    """forwarding control keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 refresh", callback_data="refresh_forward"),
            InlineKeyboardButton("⏸️ pause", callback_data="pause_forward")
        ],
        [
            InlineKeyboardButton("⏹️ stop", callback_data="stop_forward"),
            InlineKeyboardButton("📊 details", callback_data="forward_details")
        ],
        [InlineKeyboardButton("🏠 main menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """back button keyboard"""
    keyboard = [[InlineKeyboardButton("🔙 back", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)
