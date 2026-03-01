from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import logging
from config import API_ID, API_HASH, BOT_TOKEN, LINK_PATTERNS, WARN_MESSAGE, DELETE_MESSAGE, WARN_LIMIT, PENALTY_ACTION, USER_WARNINGS

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create the bot client
app = Client(
    "bio_link_detector",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Compile all link patterns
link_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in LINK_PATTERNS]

async def is_admin(client, chat_id, user_id):
    """Check if user has admin rights in the chat"""
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        return chat_member.status in ['administrator', 'creator']
    except Exception:
        return False

async def has_change_info_permission(client, chat_id, user_id):
    """Check if user has permission to change group info"""
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        logger.info(f"Checking permissions for user {user_id} in chat {chat_id}: status = {chat_member.status}")
        
        # Creator always has permission
        if chat_member.status == 'creator':
            logger.info(f"User {user_id} is creator, has permission")
            return True
        
        # Check if user is admin with change_info permission
        if chat_member.status == 'administrator':
            # Check specific permissions (change_info is usually True for full admins)
            can_change_info = getattr(chat_member, 'can_change_info', False)
            logger.info(f"User {user_id} is admin, can_change_info: {can_change_info}")
            return can_change_info or True  # Most admins can change info by default
        
        logger.info(f"User {user_id} is not creator or admin, no permission")
        return False
    except Exception as e:
        logger.error(f"Error checking permissions for user {user_id} in chat {chat_id}: {e}")
        return False

async def is_admin_or_owner(client, chat_id, user_id):
    """Check if user is group owner or admin"""
    try:
        chat_member = await client.get_chat_member(chat_id, user_id)
        return chat_member.status in ['creator', 'administrator']
    except Exception:
        return False

def has_links_in_bio(bio_text):
    """Check if the bio contains any links"""
    if not bio_text:
        return False
    
    bio_lower = bio_text.lower()
    for pattern in link_patterns:
        if pattern.search(bio_lower):
            return True
    return False

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

async def take_penalty_action(client, chat_id, user_id, sent_message, warn_msg):
    """Take the configured penalty action against the user"""
    global USER_WARNINGS
    
    if PENALTY_ACTION == "ban":
        try:
            await client.ban_chat_member(chat_id, user_id)
            await sent_message.edit_text(
                f"{warn_msg}\n\n🚫 User has been banned for having links in bio after {WARN_LIMIT} warnings."
            )
        except Exception as e:
            logger.error(f"Could not ban user: {e}")
            await sent_message.edit_text(
                f"{warn_msg}\n\n❌ Failed to ban user: {str(e)}"
            )
    elif PENALTY_ACTION == "kick":
        try:
            await client.ban_chat_member(chat_id, user_id)
            # Unban to kick (remove from chat temporarily)
            await client.unban_chat_member(chat_id, user_id)
            await sent_message.edit_text(
                f"{warn_msg}\n\n👢 User has been kicked for having links in bio after {WARN_LIMIT} warnings."
            )
        except Exception as e:
            logger.error(f"Could not kick user: {e}")
            await sent_message.edit_text(
                f"{warn_msg}\n\n❌ Failed to kick user: {str(e)}"
            )
    elif PENALTY_ACTION == "mute":
        try:
            # Mute for 24 hours (86400 seconds)
            await client.restrict_chat_member(chat_id, user_id, until_date=86400)
            await sent_message.edit_text(
                f"{warn_msg}\n\n🔇 User has been muted for 24 hours for having links in bio after {WARN_LIMIT} warnings."
            )
        except Exception as e:
            logger.error(f"Could not mute user: {e}")
            await sent_message.edit_text(
                f"{warn_msg}\n\n❌ Failed to mute user: {str(e)}"
            )
    elif PENALTY_ACTION == "warn_only":
        try:
            await sent_message.edit_text(
                f"{warn_msg}\n\n⚠️ Maximum warning reached! Taking no further action."
            )
        except Exception as e:
            logger.error(f"Could not update warning message: {e}")
    
    # Reset warning count after penalty
    if user_id in USER_WARNINGS:
        del USER_WARNINGS[user_id]

@app.on_message(filters.group & filters.new_chat_members)
async def check_new_member(client, message):
    """Check new members when they join the group"""
    try:
        for new_member in message.new_chat_members:
            user_id = new_member.id
            
            # Get user's bio/profile
            try:
                user = await client.get_chat(user_id)
                bio = getattr(user, 'bio', None)
                
                if bio and has_links_in_bio(bio):
                    # Increment warning count for the user
                    if user_id not in USER_WARNINGS:
                        USER_WARNINGS[user_id] = 0
                    USER_WARNINGS[user_id] += 1
                    
                    # Send warning message
                    warn_msg = WARN_MESSAGE.format(user_id=user_id)
                    sent_message = await message.reply_text(f"{warn_msg} ({USER_WARNINGS[user_id]}/{WARN_LIMIT})")
                    
                    # Delete the original message if configured
                    if DELETE_MESSAGE:
                        try:
                            await message.delete()
                        except Exception as e:
                            logger.warning(f"Could not delete message: {e}")
                    
                    # Take penalty action if warning limit reached
                    if USER_WARNINGS[user_id] >= WARN_LIMIT:
                        await take_penalty_action(client, message.chat.id, user_id, sent_message, warn_msg)
                    
            except Exception as e:
                logger.error(f"Error checking user {user_id}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error in new member handler: {e}")

@app.on_message(filters.group)
async def check_message_sender(client, message):
    """Check message senders for links in bio"""
    # Skip if it's a service message or the sender is None
    if not message.from_user or message.from_user.is_bot:
        return
    
    user_id = message.from_user.id
    
    try:
        # Get user's bio/profile
        user = await client.get_chat(user_id)
        bio = getattr(user, 'bio', None)
        
        if bio and has_links_in_bio(bio):
            # Increment warning count for the user
            if user_id not in USER_WARNINGS:
                USER_WARNINGS[user_id] = 0
            USER_WARNINGS[user_id] += 1
            
            # Send warning message
            warn_msg = WARN_MESSAGE.format(user_id=user_id)
            sent_message = await message.reply_text(f"{warn_msg} ({USER_WARNINGS[user_id]}/{WARN_LIMIT})")
            
            # Delete the original message if configured
            if DELETE_MESSAGE:
                try:
                    await message.delete()
                except Exception as e:
                    logger.warning(f"Could not delete message: {e}")
            
            # Take penalty action if warning limit reached
            if USER_WARNINGS[user_id] >= WARN_LIMIT:
                await take_penalty_action(client, message.chat.id, user_id, sent_message, warn_msg)
                
    except Exception as e:
        logger.error(f"Error checking user {user_id}: {e}")

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """Handle /start command"""
    # Get bot username
    bot_info = await client.get_me()
    bot_username = bot_info.username or "BioLinkRestrictorBot"  # fallback username
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("♛ Add to Group", url=f"https://t.me/{bot_username}?startgroup=new")],
        [InlineKeyboardButton("⚙️ Bot Settings", callback_data="open_settings")],
        [InlineKeyboardButton("📚 Help", callback_data="show_help")]
    ])
    
    # Get bot name and user name
    bot_name = bot_info.first_name or "Bio Link Checker"
    user_name = message.from_user.first_name or "User"
    
    start_message = (
        f"🔗 {bot_name}🔒\n"
        f"👋 Hello! {user_name} I am an Automatic Bio Link Checker Bot.\n\n"
        "🚫 I Detect And Restrict Users With Links In Their Bio.\n\n"
        "🛡 Perfect For:\n"
        "• Secure Groups\n"
        "• Anti-Spam Control\n"
        "• Clean Communities\n\n"
        "⚡ How To Use:\n"
        "1️⃣ Add Me To Your Group\n"
        "2️⃣ Give Me Admin Permission\n"
        "3️⃣ Enjoy Automatic Protection🔥\n\n"
        "🔒 I Keep Your Group Safe From Link Spammers!"
    )
    
    await message.reply_text(start_message, reply_markup=keyboard)


@app.on_message(filters.command("settings"))
async def settings_command(client, message):
    """Handle /settings command"""
    logger.info(f"Settings command received from user {message.from_user.id} in chat {message.chat.id} (type: {message.chat.type})")
    
    # Allow in private or group chats, but with different permission levels
    if message.chat.type == "private":
        # In private chats, deny access - settings only work in groups
        logger.info("Private chat detected, denying access")
        await message.reply_text("❌ Settings can only be accessed in group chats by group owners!")
        return
    else:
        # In groups, only users with change info permission can access settings
        has_permission = await has_change_info_permission(client, message.chat.id, message.from_user.id)
        logger.info(f"Group chat detected. User {message.from_user.id} has change info permission: {has_permission}")
        if not has_permission:
            await message.reply_text("❌ Only group admins with change info permission can access settings!")
            return
    
    # Create keyboard with Open Here and Open in Private buttons
    settings_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔧 Open Here", callback_data="open_settings_here")],
        [InlineKeyboardButton("🔒 Open in Private", callback_data="open_settings_private")]
    ])
    
    await message.reply_text(
        "⚙️ **Bot Settings Panel**\n\n"
        f"Current Warning Limit: {WARN_LIMIT}\n"
        f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
        "Choose how to open the settings:",
        reply_markup=settings_keyboard
    )

@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    """Handle /help command"""
    help_text = (
        "🤖 **Bio Link Restrictor Bot Help**\n\n"
        "I automatically detect and restrict users who have links in their Telegram bio.\n\n"
        "**Features:**\n"
        "• Monitor new group members\n"
        "• Check existing members when they send messages\n"
        "• Remove messages from users with links in bio\n"
        "• Configurable warning system\n\n"
        "**Permissions:**\n"
        "• Only group admins with change info permission can access settings\n"
        "• Use /settings command in group chats\n\n"
        "**Commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/settings - Access bot settings (admin only)\n\n"
        "Add me to your group and I'll start protecting it immediately!"
    )
    await message.reply_text(help_text)

@app.on_callback_query()
async def callback_handler(client, callback_query):
    """Handle callback queries from inline keyboards"""
    global WARN_LIMIT, PENALTY_ACTION
    user_id = callback_query.from_user.id
    
    # Handle help button
    if callback_query.data == "show_help":
        help_text = (
            "🤖 **Bio Link Restrictor Bot Help**\n\n"
            "I automatically detect and restrict users who have links in their Telegram bio.\n\n"
            "**Features:**\n"
            "• Monitor new group members\n"
            "• Check existing members when they send messages\n"
            "• Remove messages from users with links in bio\n"
            "• Configurable warning system\n\n"
            "**Permissions:**\n"
            "• Only group admins with change info permission can access settings\n"
            "• Use /settings command in group chats\n\n"
            "**Commands:**\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/settings - Access bot settings (admin only)\n\n"
            "Add me to your group and I'll start protecting it immediately!"
        )
        await callback_query.message.edit_text(help_text)
        await callback_query.answer()
        return
    

    
    # Handle settings button click (if we want to implement direct settings access)
    if callback_query.data == "open_settings":
        await callback_query.answer("Please use /settings command in a group chat where you have admin rights!", show_alert=True)
        return
    
    # Handle the Open Here and Open in Private buttons from settings command
    if callback_query.data == "open_settings_here" or callback_query.data == "open_settings_private":
        user_id = callback_query.from_user.id
        
        # Check permissions for the settings
        if not await has_change_info_permission(client, callback_query.message.chat.id, user_id):
            await callback_query.answer("❌ Only group admins with change info permission can use these settings!", show_alert=True)
            return
        
        # Create the actual settings keyboard
        keyboard = await get_settings_keyboard()
        await callback_query.message.edit_text(
            "⚙️ **Bot Settings Panel**\n\n"
            f"Current Warning Limit: {WARN_LIMIT}\n"
            f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
            "Use the buttons below to adjust settings:",
            reply_markup=keyboard
        )
        
        if callback_query.data == "open_settings_here":
            await callback_query.answer("🔧 Opening settings here in the group")
        else:
            # Send settings to private chat
            await client.send_message(
                user_id,
                "⚙️ **Bot Settings Panel**\n\n"
                f"Current Warning Limit: {WARN_LIMIT}\n"
                f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
                "Use the buttons below to adjust settings:",
                reply_markup=keyboard
            )
            await callback_query.answer("🔒 Settings sent to your private chat")
        return
    
    # Check if user has permission (only group owner can access settings)
    # For private chats, deny access
    if callback_query.message.chat.type == "private":
        await callback_query.answer("❌ Settings can only be accessed in group chats by group owners!", show_alert=True)
        return
    else:
        # In group chats, only users with change info permission can access settings
        user_id = callback_query.from_user.id
        if not await has_change_info_permission(client, callback_query.message.chat.id, user_id):
            await callback_query.answer("❌ Only group admins with change info permission can use these settings!", show_alert=True)
            return
    
    if callback_query.data == "increase_warn_limit":
        WARN_LIMIT += 1
        keyboard = await get_settings_keyboard()
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        await callback_query.answer(f"✅ Warning limit increased to {WARN_LIMIT}")
        
    elif callback_query.data == "decrease_warn_limit":
        if WARN_LIMIT > 1:
            WARN_LIMIT -= 1
            keyboard = await get_settings_keyboard()
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)
            await callback_query.answer(f"✅ Warning limit decreased to {WARN_LIMIT}")
        else:
            await callback_query.answer("❌ Warning limit cannot be less than 1!", show_alert=True)
            
    elif callback_query.data == "warn_limit_info":
        await callback_query.answer(f"Current warning limit: {WARN_LIMIT}", show_alert=True)
        
    elif callback_query.data == "penalty_info":
        await callback_query.answer(f"Current penalty: {PENALTY_ACTION.upper()}", show_alert=True)
        
    elif callback_query.data == "change_penalty":
        # Create penalty selection keyboard
        penalty_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔨 Ban User", callback_data="set_penalty_ban")],
            [InlineKeyboardButton("🔇 Mute User", callback_data="set_penalty_mute")],
            [InlineKeyboardButton("👢 Kick User", callback_data="set_penalty_kick")],
            [InlineKeyboardButton("⚠️ Warning Only", callback_data="set_penalty_warn")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="back_to_settings")]
        ])
        await callback_query.message.edit_text(
            "📋 **Select Penalty Action**\n\n"
            f"Current Penalty: {PENALTY_ACTION.upper()}\n\n"
            "Choose the action to take when warning limit is reached:",
            reply_markup=penalty_keyboard
        )
        await callback_query.answer()
        
    elif callback_query.data.startswith("set_penalty_"):
        if callback_query.data == "set_penalty_ban":
            PENALTY_ACTION = "ban"
        elif callback_query.data == "set_penalty_mute":
            PENALTY_ACTION = "mute"
        elif callback_query.data == "set_penalty_kick":
            PENALTY_ACTION = "kick"
        elif callback_query.data == "set_penalty_warn":
            PENALTY_ACTION = "warn_only"
        
        # Go back to settings menu
        keyboard = await get_settings_keyboard()
        await callback_query.message.edit_text(
            "⚙️ **Bot Settings Panel**\n\n"
            f"Current Warning Limit: {WARN_LIMIT}\n"
            f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
            "Use the buttons below to adjust settings:",
            reply_markup=keyboard
        )
        await callback_query.answer(f"✅ Penalty action set to {PENALTY_ACTION.upper()}")
        
    elif callback_query.data == "back_to_settings":
        keyboard = await get_settings_keyboard()
        await callback_query.message.edit_text(
            "⚙️ **Bot Settings Panel**\n\n"
            f"Current Warning Limit: {WARN_LIMIT}\n"
            f"Current Penalty Action: {PENALTY_ACTION.upper()}\n\n"
            "Use the buttons below to adjust settings:",
            reply_markup=keyboard
        )
        await callback_query.answer()
        return
    

if __name__ == "__main__":
    logger.info("Starting Bio Link Restrictor Bot...")
    app.run()