# ⚡ Advanced Auto Forward Bot

> Ultra Fast Telegram Auto Forwarding Bot with Force Join, AI Welcome Messages & Advanced Features

---

## 🚀 Features

- ✅ **Ultra Fast Forwarding** — Near-instant message forwarding
- ✅ **Force Join** — User must join channel before using bot
- ✅ **Smart Processing Flow** — Message edits from "Processing..." → Access Granted/Denied
- ✅ **Welcome Image** — Beautiful welcome with custom image
- ✅ **Colorful Buttons** — Developer, Support Group, Channel, YouTube, Help, About, Settings
- ✅ **Keyword Filtering** — Forward only specific messages
- ✅ **Multi-Channel** — Multiple sources & destinations
- ✅ **Admin Panel** — Stats, Ban/Unban, Broadcast
- ✅ **Media Support** — Photos, Videos, Files all forwarded

---

## 📁 Files

| File | Description |
|------|-------------|
| `bot.py` | Main bot logic |
| `config.py` | All settings & customization |
| `requirements.txt` | Python dependencies |

---

## ⚙️ Setup

### Step 1 — Get Credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Create an App → get `API_ID` and `API_HASH`
3. Create a bot via [@BotFather](https://t.me/BotFather) → get `BOT_TOKEN`

### Step 2 — Edit config.py

Open `config.py` and fill in:

```python
BOT_TOKEN = "your_bot_token"
API_ID    = 123456
API_HASH  = "your_api_hash"
OWNER_ID  = your_telegram_id   # Get from @userinfobot

FORCE_JOIN_CHANNEL = "@your_channel"
FORCE_JOIN_LINK    = "https://t.me/your_channel"

SOURCE_CHANNELS      = [-100xxxxxxxxxx]
DESTINATION_CHANNELS = [-100xxxxxxxxxx]

WELCOME_IMAGE = "https://telegra.ph/your-image-link"
```

### Step 3 — Install & Run

```bash
# Install Python 3.10+
pip install -r requirements.txt

# Run the bot
python bot.py
```

### Step 4 — Deploy on GitHub + Railway/VPS

1. Push all files to GitHub
2. Deploy on [Railway.app](https://railway.app) or any VPS
3. Set environment variables or keep config.py

---

## 🔒 Force Join Flow

```
User sends /start
     ↓
Bot sends "⚙️ Processing..." message
     ↓
Bot checks if user joined @channel
     ↓
  [Joined?]
  YES → Edit message → "✅ Access Granted!" + Full Menu
  NO  → Edit message → "❌ Join Channel" + Join Button
     ↓
User clicks "🔄 I Joined — Check Again"
     ↓
Bot re-checks → Same flow
```

---

## 📝 Customization

All text, messages, and links are in `config.py`. Just edit:

- `WELCOME_MSG` — Welcome text
- `JOINED_MSG` — After joining message  
- `NOT_JOINED_MSG` — Force join message
- `HELP_MSG` — Help text
- `ABOUT_MSG` — About text
- Button URLs (Developer, Group, Channel, YouTube)

---

## 👑 Admin Commands

| Command | Description |
|---------|-------------|
| `/stats` | View bot statistics |
| `/ban <id>` | Ban a user |
| `/unban <id>` | Unban a user |
| `/broadcast <msg>` | Broadcast to all users |

---

## 💡 Tips

- Use [@userinfobot](https://t.me/userinfobot) to get your Telegram ID
- Use [@username_to_id_bot](https://t.me/username_to_id_bot) to get channel IDs
- Upload welcome image to [telegra.ph](https://telegra.ph) and paste the link
- Add bot as **Admin** in source & destination channels

---

Made with ❤️ 
# Boss-Forward-Bot
