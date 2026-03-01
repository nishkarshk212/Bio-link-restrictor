#!/usr/bin/env python3
"""
Minimal test bot with just the settings command
"""
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from config import API_ID, API_HASH, BOT_TOKEN, WARN_LIMIT, PENALTY_ACTION

# Create the bot client
app = Client(
    "test_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def get_settings_keyboard():
    """Create inline keyboard for settings panel"""
    keyboard = [
        [
            InlineKeyboardButton("➖ Warn Limit", callback_data="decrease_warn_limit"),
            InlineKeyboardButton(f"Warn Limit: {WARN_LIMIT}", callback_data="warn_limit_info"),
            InlineKeyboardButton("➕ Warn Limit", callback_data="increase_warn_limit")
        ],
        [
            InlineKeyboardButton(f"Penalty: {PENALTY_ACTION.upper()}", callback_data="penalty_info"),
        ],
        [
            InlineKeyboardButton("📋 Change Penalty", callback_data="change_penalty")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def is_group_owner(client, chat_id, user_id):
    """Check if user is the group owner (creator)"""
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        return chat_member.status == 'creator'
    except Exception:
        return False

@app.on_message(filters.command("settings"))
async def settings_command(client, message):
    """Handle /settings command"""
    logger.info(f"Settings command received from user {message.from_user.id} in chat {message.chat.id} (type: {message.chat.type})")
    
    # Allow in private or group chats, but with different permission levels
    if message.chat.type == "private":
        # In private chats, only allow if user is a group owner of any group with this bot
        logger.info("Private chat detected, denying access")
        await message.reply_text("❌ Settings can only be accessed in group chats by group owners!")
        return
    else:
        # In groups, only group owner (creator) can access settings
        is_owner = await is_group_owner(client, message.chat.id, message.from_user.id)
        logger.info(f"Group chat detected. User {message.from_user.id} is owner: {is_owner}")
        if not is_owner:
            await message.reply_text("❌ Only the group owner can access settings!")
            return
    
    keyboard = await get_settings_keyboard()
    await message.reply_text(
        "⚙️ **Bot Settings Panel**\n\n"
        f"Current Warning Limit: {WARN_LIMIT}\n"
        f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
        "Use the buttons below to adjust settings:",
        reply_markup=keyboard
    )

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """Handle /start command"""
    await message.reply_text(
        "👋 Hello! I'm a test bot for settings command.\n\n"
        "Send /settings in a group where you're the owner to test the settings panel."
    )

if __name__ == "__main__":
    logger.info("Starting Test Bot...")
    app.run()