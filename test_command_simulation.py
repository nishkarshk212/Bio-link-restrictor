#!/usr/bin/env python3
"""
Test script to simulate settings command execution
"""
import asyncio
from pyrogram import Client
from pyrogram.types import Message, User, Chat
from config import API_ID, API_HASH, BOT_TOKEN
import importlib.util
import sys

# Import the bot module
spec = importlib.util.spec_from_file_location("bot", "bot.py")
bot_module = importlib.util.module_from_spec(spec)
sys.modules["bot"] = bot_module
spec.loader.exec_module(bot_module)

async def test_settings_command_simulation():
    """Test the settings command by simulating a message"""
    print("🔍 Testing Settings Command Simulation...")
    print("=" * 50)
    
    # Create a mock message
    async with Client("test_client", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as client:
        # Create mock objects
        mock_user = User(
            id=123456789,  # Test user ID
            is_self=False,
            is_contact=False,
            is_mutual_contact=False,
            is_deleted=False,
            is_bot=False,
            is_verified=False,
            is_restricted=False,
            is_scam=False,
            is_fake=False,
            is_support=False,
            is_premium=False,
            first_name="Test",
            last_name="User",
            status="offline",
            dc_id=1,
            username="testuser"
        )
        
        mock_chat = Chat(
            id=-1001234567890,  # Test group ID (negative for groups)
            type="group",
            title="Test Group",
            username="testgroup"
        )
        
        # Create mock message
        mock_message = Message(
            id=1,
            from_user=mock_user,
            chat=mock_chat,
            date=1234567890,
            text="/settings"
        )
        
        print(f"Created mock message:")
        print(f"  User ID: {mock_message.from_user.id}")
        print(f"  Chat ID: {mock_message.chat.id}")
        print(f"  Chat Type: {mock_message.chat.type}")
        print(f"  Text: {mock_message.text}")
        
        # Test the group owner checking function
        print("\nTesting group owner checking...")
        try:
            is_owner = await bot_module.is_group_owner(client, mock_chat.id, mock_user.id)
            print(f"User {mock_user.id} is group owner: {is_owner}")
        except Exception as e:
            print(f"Error checking group owner: {e}")
        
        # Test the settings command function
        print("\nTesting settings command function...")
        try:
            # This would normally be called by the handler
            await bot_module.settings_command(client, mock_message)
            print("✅ Settings command function executed without errors")
        except Exception as e:
            print(f"❌ Settings command function failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_settings_command_simulation())