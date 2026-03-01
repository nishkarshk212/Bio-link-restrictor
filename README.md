# 🤖 Telegram Bio Link Restrictor Bot

A powerful Telegram bot that automatically detects and restricts users who have links in their bio/profile description.

## 🌟 Features

- **Automatic Detection**: Monitors all group members for links in their bio
- **New Member Screening**: Checks users when they join the group
- **Active Monitoring**: Checks existing members when they send messages
- **Customizable Actions**: 
  - Send warning messages
  - Delete messages from users with bio links
  - Ban users with links in bio (optional)
- **Multiple Link Patterns**: Detects various URL formats including:
  - HTTP/HTTPS links
  - Telegram links (t.me/)
  - Shortened URLs (bit.ly, tinyurl.com, etc.)
  - And more...

## 🚀 Setup Instructions

### 1. Get Telegram API Credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Create a new application
4. Note down your `API_ID` and `API_HASH`

### 2. Create a Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Note down the `BOT_TOKEN`

### 3. Configure the Bot

Edit the `.env` file with your credentials:

```env
# Telegram Bot Configuration
API_ID=123456
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

# Bot Settings
DELETE_MESSAGE=true
BAN_USER=false
WARN_MESSAGE=⚠️ {mention}, links are not allowed in bio!
```

Alternatively, you can still edit the `config.py` file directly if you prefer.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python bot.py
```

## 🛠️ Configuration Options

### Link Detection Patterns
The bot checks for these link patterns by default:
- `https?://` - Standard HTTP/HTTPS URLs
- `t\.me/` - Telegram links
- `www\.` - Web URLs
- `telegram\.me/` - Telegram.me links
- `t\.me/joinchat/` - Telegram invite links
- `bit\.ly/` - Bit.ly shortened URLs
- `tinyurl\.com/` - TinyURL shortened URLs
- `shorturl\.at/` - ShortURL.at shortened URLs
- `go\.lan/` - Custom domain pattern

### Action Settings
- `DELETE_MESSAGE`: Delete messages from users with links in bio
- `BAN_USER`: Ban users who have links in their bio
- `WARN_MESSAGE`: Customizable warning message

## 📋 Commands

- `/start` - Start the bot (private chat)
- `/help` - Show help information (private chat)

## 🛡️ How It Works

1. When a user joins a group, the bot checks their bio
2. When existing members send messages, the bot checks their bio
3. If links are detected, the bot:
   - Sends a warning message
   - Optionally deletes the message
   - Optionally bans the user

## 🔧 Customization

You can modify the `LINK_PATTERNS` in `config.py` to add or remove detection patterns:

```python
LINK_PATTERNS = [
    r"https?://",
    r"t\.me/",
    r"www\.",
    # Add your custom patterns here
]
```

## 📝 Logging

The bot includes comprehensive logging to help you monitor its activity. Logs include:
- User detection events
- Action taken (warning, delete, ban)
- Error messages for troubleshooting

## ⚠️ Important Notes

- The bot needs admin privileges in groups to delete messages and ban users
- Make sure to add the bot as an administrator in your groups
- The bot respects Telegram's rate limits and API usage guidelines

## 🤝 Support

For issues or feature requests, please check the logs first and ensure your API credentials are correct.

## 📄 License

This project is open source and available under the MIT License.

# Bio Link Restrictor

🔗 **Automatic Bio Link Checker Bot** - A Telegram bot that detects and restricts users with links in their bio.

## 🚀 Features

- **Automatic Detection** - Monitors group members for links in their bio
- **Warning System** - Configurable warning limits before taking action
- **Flexible Penalties** - Choose from ban, mute, kick, or warning-only actions
- **Admin Controls** - Settings accessible to group admins with "change info" permission
- **Anti-Spam Protection** - Keeps your groups clean from link spammers

## ⚙️ Commands

- `/start` - Get bot information and quick access buttons
- `/help` - Show help information
- `/settings` - Access bot settings (group admins with "change info" permission only)

## 🔧 Settings Panel

The bot includes a comprehensive settings panel with:
- **Warning Limit Adjustment** - Use ➕/➖ buttons to set warning thresholds
- **Penalty Configuration** - Choose from ban, mute, kick, or warning-only actions
- **Real-time Updates** - Settings are applied immediately

## 🛡️ Permissions

- Settings access is restricted to users with "change info" admin permission in groups
- Includes group creators and admins with appropriate permissions
- Private chat access is disabled for security

## 📋 Requirements

- Python 3.7+
- Pyrogram
- TgCrypto

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/nishkarshk212/Bio-link-restrictor.git
cd Bio-link-restrictor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
DELETE_MESSAGE=true
WARN_LIMIT=3
PENALTY_ACTION=ban
WARN_MESSAGE=⚠️ User ID {user_id}, links are not allowed in bio!
```

4. Run the bot:
```bash
python bot.py
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License.
