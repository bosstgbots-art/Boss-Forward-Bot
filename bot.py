# ============================================================
#        🤖 ADVANCED AUTO FORWARD BOT - MAIN FILE
#        Developed by: @YourUsername
#        Version: 2.0 Ultra Advanced
#        
#        Features:
#        ✅ Ultra Fast Forwarding
#        ✅ Force Join with Smart Check
#        ✅ Welcome Image + AI Messages
#        ✅ Processing Message (Edit Flow)
#        ✅ Colorful Buttons Menu
#        ✅ Admin Panel
#        ✅ Keyword Filtering
#        ✅ Multi Channel Support
#        ✅ Ban/Unban System
#        ✅ Broadcast System
#        ✅ Bot Statistics
# ============================================================

import asyncio
import logging
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)
from pyrogram.errors import (
    UserNotParticipant, ChatAdminRequired,
    FloodWait, UserBanned
)
import config

# ──────────────────────────────────────────────
#  📋 LOGGING SETUP
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
#  🤖 BOT CLIENT
# ──────────────────────────────────────────────
app = Client(
    "auto_forward_bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)

# ──────────────────────────────────────────────
#  💾 IN-MEMORY DATABASE (simple)
# ──────────────────────────────────────────────
banned_users     = set()
bot_stats        = {"total_users": 0, "forwarded": 0, "start_time": datetime.now()}
registered_users = set()

# ──────────────────────────────────────────────
#  🛠️ HELPER FUNCTIONS
# ──────────────────────────────────────────────

async def is_member(client: Client, user_id: int) -> bool:
    """Check if user is member of force join channel."""
    try:
        member = await client.get_chat_member(config.FORCE_JOIN_CHANNEL, user_id)
        return member.status not in [
            enums.ChatMemberStatus.BANNED,
            enums.ChatMemberStatus.LEFT
        ]
    except UserNotParticipant:
        return False
    except Exception as e:
        logger.error(f"Membership check error: {e}")
        return False


def is_admin(user_id: int) -> bool:
    """Check if user is admin or owner."""
    return user_id in config.ADMIN_IDS or user_id == config.OWNER_ID


def build_main_menu() -> InlineKeyboardMarkup:
    """Build colorful main menu buttons."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👨‍💻 Developer",    url=f"https://t.me/{config.DEVELOPER_USERNAME.lstrip('@')}"),
            InlineKeyboardButton("💬 Support Group",  url=config.SUPPORT_GROUP),
        ],
        [
            InlineKeyboardButton("📢 Support Channel", url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton("🎥 YouTube Channel", url=config.YOUTUBE_CHANNEL),
        ],
        [
            InlineKeyboardButton("❓ Help",    callback_data="help"),
            InlineKeyboardButton("ℹ️ About",   callback_data="about"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        ],
    ])


def build_join_button() -> InlineKeyboardMarkup:
    """Build force join button."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Join Channel Now", url=config.FORCE_JOIN_LINK),
        ],
        [
            InlineKeyboardButton("🔄 I Joined — Check Again", callback_data="check_join"),
        ],
    ])


def build_back_button() -> InlineKeyboardMarkup:
    """Back to main menu button."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
    ])


# ──────────────────────────────────────────────
#  🚀 /START COMMAND
# ──────────────────────────────────────────────
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user_id   = message.from_user.id
    user_name = message.from_user.first_name

    # Track user
    if user_id not in registered_users:
        registered_users.add(user_id)
        bot_stats["total_users"] += 1

    # Check if banned
    if user_id in banned_users:
        await message.reply("🚫 <b>You are banned from using this bot.</b>", parse_mode=enums.ParseMode.HTML)
        return

    # Send processing message first
    proc_msg = await message.reply(
        config.PROCESSING_MSG,
        parse_mode=enums.ParseMode.HTML
    )

    await asyncio.sleep(1.5)  # Short delay for effect

    # Check force join
    joined = await is_member(client, user_id)

    if not joined:
        # Edit processing msg → not joined
        await proc_msg.edit_text(
            config.NOT_JOINED_MSG,
            reply_markup=build_join_button(),
            parse_mode=enums.ParseMode.HTML
        )
        return

    # User is joined — delete processing msg, send welcome
    await proc_msg.delete()

    welcome_text = config.WELCOME_MSG.format(
        bot_name=config.BOT_NAME,
        version=config.BOT_VERSION,
        developer=config.DEVELOPER_USERNAME,
        user=user_name
    )

    # Send welcome image with caption
    try:
        await client.send_photo(
            chat_id=user_id,
            photo=config.WELCOME_IMAGE,
            caption=welcome_text,
            reply_markup=build_main_menu(),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        # If image fails, send text only
        await message.reply(
            welcome_text,
            reply_markup=build_main_menu(),
            parse_mode=enums.ParseMode.HTML
        )


# ──────────────────────────────────────────────
#  🔄 CHECK JOIN CALLBACK
# ──────────────────────────────────────────────
@app.on_callback_query(filters.regex("^check_join$"))
async def check_join_callback(client: Client, query: CallbackQuery):
    user_id   = query.from_user.id
    user_name = query.from_user.first_name

    # Edit to processing
    await query.message.edit_text(
        config.PROCESSING_MSG,
        parse_mode=enums.ParseMode.HTML
    )

    await asyncio.sleep(2)

    joined = await is_member(client, user_id)

    if joined:
        # ✅ Access Granted
        await query.message.edit_text(
            config.JOINED_MSG.format(bot_name=config.BOT_NAME, user=user_name),
            reply_markup=build_main_menu(),
            parse_mode=enums.ParseMode.HTML
        )
        # Send welcome image separately
        try:
            await client.send_photo(
                chat_id=user_id,
                photo=config.WELCOME_IMAGE,
                caption=f"🎉 <b>Welcome {user_name}!</b>\n\nYou now have full access to <b>{config.BOT_NAME}</b>!",
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass
    else:
        # ❌ Still not joined
        await query.message.edit_text(
            config.NOT_JOINED_MSG,
            reply_markup=build_join_button(),
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer("❌ You haven't joined yet!", show_alert=True)


# ──────────────────────────────────────────────
#  📋 CALLBACK QUERIES (Menu Buttons)
# ──────────────────────────────────────────────
@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_callback(client: Client, query: CallbackQuery):
    await query.message.edit_caption(
        caption=config.WELCOME_MSG.format(
            bot_name=config.BOT_NAME,
            version=config.BOT_VERSION,
            developer=config.DEVELOPER_USERNAME,
            user=query.from_user.first_name
        ),
        reply_markup=build_main_menu(),
        parse_mode=enums.ParseMode.HTML
    ) if query.message.photo else await query.message.edit_text(
        config.WELCOME_MSG.format(
            bot_name=config.BOT_NAME,
            version=config.BOT_VERSION,
            developer=config.DEVELOPER_USERNAME,
            user=query.from_user.first_name
        ),
        reply_markup=build_main_menu(),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_callback_query(filters.regex("^help$"))
async def help_callback(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        config.HELP_MSG,
        reply_markup=build_back_button(),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_callback_query(filters.regex("^about$"))
async def about_callback(client: Client, query: CallbackQuery):
    await query.message.edit_text(
        config.ABOUT_MSG.format(
            bot_name=config.BOT_NAME,
            version=config.BOT_VERSION,
            developer=config.DEVELOPER_USERNAME
        ),
        reply_markup=build_back_button(),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_callback_query(filters.regex("^settings$"))
async def settings_callback(client: Client, query: CallbackQuery):
    if not is_admin(query.from_user.id):
        await query.answer("⚠️ Only admins can access settings!", show_alert=True)
        return

    settings_text = f"""⚙️ <b>Bot Settings</b>

━━━━━━━━━━━━━━━━━━━━━━
📤 <b>Forwarding:</b> {'✅ Active' if config.FORWARD_TEXT or config.FORWARD_MEDIA else '❌ Off'}
⚡ <b>Forward Delay:</b> {config.FORWARD_DELAY}s
📷 <b>Media Forward:</b> {'✅ Yes' if config.FORWARD_MEDIA else '❌ No'}
🔒 <b>Force Join:</b> ✅ {config.FORCE_JOIN_CHANNEL}
📊 <b>Total Users:</b> {bot_stats['total_users']}
📨 <b>Forwarded:</b> {bot_stats['forwarded']}
━━━━━━━━━━━━━━━━━━━━━━"""

    await query.message.edit_text(
        settings_text,
        reply_markup=build_back_button(),
        parse_mode=enums.ParseMode.HTML
    )


# ──────────────────────────────────────────────
#  📖 /HELP COMMAND
# ──────────────────────────────────────────────
@app.on_message(filters.command("help") & filters.private)
async def help_handler(client: Client, message: Message):
    await message.reply(
        config.HELP_MSG,
        reply_markup=build_back_button(),
        parse_mode=enums.ParseMode.HTML
    )


# ──────────────────────────────────────────────
#  ℹ️ /ABOUT COMMAND
# ──────────────────────────────────────────────
@app.on_message(filters.command("about") & filters.private)
async def about_handler(client: Client, message: Message):
    await message.reply(
        config.ABOUT_MSG.format(
            bot_name=config.BOT_NAME,
            version=config.BOT_VERSION,
            developer=config.DEVELOPER_USERNAME
        ),
        reply_markup=build_back_button(),
        parse_mode=enums.ParseMode.HTML
    )


# ──────────────────────────────────────────────
#  📊 /STATUS COMMAND
# ──────────────────────────────────────────────
@app.on_message(filters.command("status") & filters.private)
async def status_handler(client: Client, message: Message):
    user_id = message.from_user.id
    joined  = await is_member(client, user_id)
    uptime  = datetime.now() - bot_stats["start_time"]

    status_text = f"""📊 <b>Your Status</b>

━━━━━━━━━━━━━━━━━━━━━━
👤 <b>User ID:</b> <code>{user_id}</code>
✅ <b>Channel Member:</b> {'Yes ✅' if joined else 'No ❌'}
🚫 <b>Banned:</b> {'Yes ❌' if user_id in banned_users else 'No ✅'}
━━━━━━━━━━━━━━━━━━━━━━
🤖 <b>Bot Uptime:</b> {str(uptime).split('.')[0]}
📨 <b>Messages Forwarded:</b> {bot_stats['forwarded']}
👥 <b>Total Users:</b> {bot_stats['total_users']}
━━━━━━━━━━━━━━━━━━━━━━"""

    await message.reply(status_text, parse_mode=enums.ParseMode.HTML)


# ──────────────────────────────────────────────
#  👑 ADMIN: /STATS
# ──────────────────────────────────────────────
@app.on_message(filters.command("stats") & filters.private)
async def stats_handler(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⚠️ <b>Admin only command!</b>", parse_mode=enums.ParseMode.HTML)
        return

    uptime = datetime.now() - bot_stats["start_time"]
    stats_text = f"""📊 <b>Bot Statistics</b>

━━━━━━━━━━━━━━━━━━━━━━
👥 <b>Total Users:</b> {bot_stats['total_users']}
📨 <b>Forwarded Messages:</b> {bot_stats['forwarded']}
🚫 <b>Banned Users:</b> {len(banned_users)}
⏱️ <b>Uptime:</b> {str(uptime).split('.')[0]}
📅 <b>Started:</b> {bot_stats['start_time'].strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━
📤 <b>Source Channels:</b> {len(config.SOURCE_CHANNELS)}
📥 <b>Destination Channels:</b> {len(config.DESTINATION_CHANNELS)}
━━━━━━━━━━━━━━━━━━━━━━"""

    await message.reply(stats_text, parse_mode=enums.ParseMode.HTML)


# ──────────────────────────────────────────────
#  👑 ADMIN: /BAN & /UNBAN
# ──────────────────────────────────────────────
@app.on_message(filters.command("ban") & filters.private)
async def ban_handler(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⚠️ <b>Admin only!</b>", parse_mode=enums.ParseMode.HTML)
        return
    try:
        target_id = int(message.command[1])
        banned_users.add(target_id)
        await message.reply(f"🚫 <b>User <code>{target_id}</code> has been banned.</b>", parse_mode=enums.ParseMode.HTML)
    except (IndexError, ValueError):
        await message.reply("❌ Usage: /ban <user_id>", parse_mode=enums.ParseMode.HTML)


@app.on_message(filters.command("unban") & filters.private)
async def unban_handler(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⚠️ <b>Admin only!</b>", parse_mode=enums.ParseMode.HTML)
        return
    try:
        target_id = int(message.command[1])
        banned_users.discard(target_id)
        await message.reply(f"✅ <b>User <code>{target_id}</code> has been unbanned.</b>", parse_mode=enums.ParseMode.HTML)
    except (IndexError, ValueError):
        await message.reply("❌ Usage: /unban <user_id>", parse_mode=enums.ParseMode.HTML)


# ──────────────────────────────────────────────
#  👑 ADMIN: /BROADCAST
# ──────────────────────────────────────────────
@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client: Client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply("⚠️ <b>Admin only!</b>", parse_mode=enums.ParseMode.HTML)
        return

    if len(message.command) < 2:
        await message.reply("❌ Usage: /broadcast <your message>", parse_mode=enums.ParseMode.HTML)
        return

    broadcast_text = message.text.split(None, 1)[1]
    sent_count  = 0
    fail_count  = 0

    status_msg = await message.reply("📡 <b>Broadcasting...</b>", parse_mode=enums.ParseMode.HTML)

    for user_id in registered_users:
        try:
            await client.send_message(
                user_id,
                f"📢 <b>Broadcast Message</b>\n\n{broadcast_text}",
                parse_mode=enums.ParseMode.HTML
            )
            sent_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"📤 Sent: {sent_count}\n❌ Failed: {fail_count}",
        parse_mode=enums.ParseMode.HTML
    )


# ──────────────────────────────────────────────
#  ⚡ ULTRA FAST AUTO FORWARDING
# ──────────────────────────────────────────────
@app.on_message(filters.chat(config.SOURCE_CHANNELS))
async def auto_forward_handler(client: Client, message: Message):
    """Ultra fast message forwarder from source to destination channels."""

    # Keyword filter check
    if config.FILTER_KEYWORDS:
        msg_text = message.text or message.caption or ""
        if not any(kw.lower() in msg_text.lower() for kw in config.FILTER_KEYWORDS):
            return

    # Block keyword check
    if config.BLOCK_KEYWORDS:
        msg_text = message.text or message.caption or ""
        if any(kw.lower() in msg_text.lower() for kw in config.BLOCK_KEYWORDS):
            return

    # Media type check
    if message.media and not config.FORWARD_MEDIA:
        return
    if not message.media and not config.FORWARD_TEXT:
        return

    # Forward to all destinations
    for dest in config.DESTINATION_CHANNELS:
        try:
            if config.FORWARD_DELAY > 0:
                await asyncio.sleep(config.FORWARD_DELAY)

            # Custom caption handling
            if config.REMOVE_CAPTION and message.caption:
                await message.copy(dest, caption="")
            elif config.ADD_CAPTION and not message.caption:
                await message.copy(dest, caption=config.ADD_CAPTION)
            else:
                await message.copy(dest)

            bot_stats["forwarded"] += 1

        except FloodWait as e:
            logger.warning(f"FloodWait: sleeping {e.value}s")
            await asyncio.sleep(e.value)
            await message.copy(dest)
        except Exception as e:
            logger.error(f"Forward error to {dest}: {e}")


# ──────────────────────────────────────────────
#  🚀 RUN BOT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════╗
║   🤖  ADVANCED AUTO FORWARD BOT     ║
║   Version: {config.BOT_VERSION:<26}║
║   Status: Starting...               ║
╚══════════════════════════════════════╝
    """)
    logger.info("Bot is starting...")
    app.run()
    logger.info("Bot stopped.")
