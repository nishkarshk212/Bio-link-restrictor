import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
API_ID = int(os.getenv('API_ID', 123456))
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
# Note: Group owner (creator) automatically has access to settings
# No specific OWNER_ID needed as group creator permissions are checked dynamically

# Bot Settings
BOT_NAME = "Bio Link Restrictor"
DELETE_MESSAGE = os.getenv('DELETE_MESSAGE', 'true').lower() == 'true'
WARN_LIMIT = int(os.getenv('WARN_LIMIT', 3))  # Number of warnings before taking action
WARN_MESSAGE = os.getenv('WARN_MESSAGE', "⚠️ User ID {user_id}, links are not allowed in bio!")
PENALTY_ACTION = os.getenv('PENALTY_ACTION', 'ban')  # Options: 'ban', 'mute', 'kick', 'warn_only'

# Store user warnings (in production, use a database)
USER_WARNINGS = {}

# Link patterns to detect
LINK_PATTERNS = [
    r"https?://",
    r"t\.me/",
    r"www\.",
    r"telegram\.me/",
    r"t\.me/joinchat/",
    r"bit\.ly/",
    r"tinyurl\.com/",
    r"shorturl\.at/",
    r"go\.lan/",
]