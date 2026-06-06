# ============================================================
#        🤖 ADVANCED AUTO FORWARD BOT - CONFIG FILE
#        Developed by: @YourUsername
#        Version: 2.0 Ultra Advanced
# ============================================================

import os

# ──────────────────────────────────────────────
#  🔑 BOT CREDENTIALS (FILL THESE)
# ──────────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"          # @BotFather se lo
API_ID    = 123456                          # my.telegram.org
API_HASH  = "YOUR_API_HASH_HERE"           # my.telegram.org

# ──────────────────────────────────────────────
#  👑 OWNER / ADMIN
# ──────────────────────────────────────────────
OWNER_ID   = 123456789          # Apna Telegram User ID
ADMIN_IDS  = [123456789]        # Extra admins (list of IDs)

# ──────────────────────────────────────────────
#  🔒 FORCE JOIN CHANNEL (ek hi rakhna)
# ──────────────────────────────────────────────
FORCE_JOIN_CHANNEL = "@YourChannelUsername"   # e.g. "@mychannel"
FORCE_JOIN_LINK    = "https://t.me/YourChannelUsername"

# ──────────────────────────────────────────────
#  📤 FORWARD SETTINGS
# ──────────────────────────────────────────────
SOURCE_CHANNELS = [
    -100xxxxxxxxxx,   # Source channel/group ID 1
    -100xxxxxxxxxx,   # Source channel/group ID 2
]

DESTINATION_CHANNELS = [
    -100xxxxxxxxxx,   # Destination channel/group ID 1
    -100xxxxxxxxxx,   # Destination channel/group ID 2
]

FORWARD_DELAY        = 0        # Seconds delay between forwards (0 = Ultra Fast)
FORWARD_MEDIA        = True     # Forward photos/videos/files
FORWARD_TEXT         = True     # Forward text messages
REMOVE_CAPTION       = False    # Remove original caption
ADD_CAPTION          = ""       # Add custom caption (blank = none)
FILTER_KEYWORDS      = []       # Only forward if contains these words (empty = all)
BLOCK_KEYWORDS       = []       # Block messages with these words

# ──────────────────────────────────────────────
#  🎨 BOT INFO / BUTTONS
# ──────────────────────────────────────────────
BOT_NAME        = "⚡ Ultra Forward Bot"
BOT_VERSION     = "v2.0 Advanced"
DEVELOPER_USERNAME  = "@YourUsername"
SUPPORT_GROUP       = "https://t.me/YourSupportGroup"
SUPPORT_CHANNEL     = "https://t.me/YourSupportChannel"
YOUTUBE_CHANNEL     = "https://youtube.com/@YourChannel"

# ──────────────────────────────────────────────
#  🖼️ WELCOME IMAGE URL
# ──────────────────────────────────────────────
WELCOME_IMAGE = "https://telegra.ph/file/your-welcome-image.jpg"
# Tip: Koi bhi image telegra.ph pe upload karke link paste karo

# ──────────────────────────────────────────────
#  💬 MESSAGES
# ──────────────────────────────────────────────
PROCESSING_MSG = "⚙️ <b>Processing...</b>\n\n<i>Please wait, checking your membership...</i>"

JOINED_MSG = """✅ <b>Access Granted!</b>

🎉 Welcome to <b>{bot_name}</b>!

You have successfully joined our community. You now have <b>full access</b> to all bot features.

⚡ <b>Ultra Fast Forwarding:</b> Active
🔒 <b>Status:</b> Verified Member
🌟 <b>Enjoy all premium features!</b>

Use /help to see all available commands."""

NOT_JOINED_MSG = """❌ <b>Access Denied!</b>

🔒 You must join our channel to use this bot.

👇 <b>Click the button below to join:</b>"""

WELCOME_MSG = """🤖 <b>Welcome to {bot_name}!</b>

<i>The most advanced auto-forwarding bot on Telegram</i>

━━━━━━━━━━━━━━━━━━━━━━
⚡ <b>Features:</b>
  • Ultra Fast Message Forwarding
  • Smart Keyword Filtering
  • Multi-Channel Support
  • Auto Media Forwarding
  • Real-time Processing
━━━━━━━━━━━━━━━━━━━━━━

🔖 <b>Version:</b> {version}
👨‍💻 <b>Developer:</b> {developer}

<i>Use the buttons below to navigate.</i>"""

HELP_MSG = """📖 <b>Help & Commands</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 <b>User Commands:</b>
  /start — Start the bot
  /help  — Show this message
  /about — Bot information
  /status — Check your status

👑 <b>Admin Commands:</b>
  /addforward — Add forward pair
  /removeforward — Remove forward pair
  /listforward — List all pairs
  /broadcast — Send broadcast
  /stats — Bot statistics
  /ban [user_id] — Ban a user
  /unban [user_id] — Unban a user
━━━━━━━━━━━━━━━━━━━━━━"""

ABOUT_MSG = """ℹ️ <b>About {bot_name}</b>

━━━━━━━━━━━━━━━━━━━━━━
🤖 <b>Bot:</b> {bot_name}
📌 <b>Version:</b> {version}
👨‍💻 <b>Developer:</b> {developer}
🌐 <b>Platform:</b> Telegram Bot API
⚙️ <b>Engine:</b> Python + Pyrogram
⚡ <b>Speed:</b> Ultra Fast
━━━━━━━━━━━━━━━━━━━━━━

<i>Built with ❤️ for the Telegram community</i>"""
