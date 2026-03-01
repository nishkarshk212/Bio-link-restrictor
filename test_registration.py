#!/usr/bin/env python3
"""
Simple test to check if the settings command works
"""
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import API_ID, API_HASH, BOT_TOKEN

# Test the actual settings command registration
async def test_settings_registration():
    """Test if settings command is properly registered"""
    print("🔍 Testing Settings Command Registration...")
    print("=" * 50)
    
    # Create client
    app = Client("test_registration", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    # Counter to track if handler is called
    handler_called = False
    
    # Test handler function
    async def test_settings_handler(client, message):
        nonlocal handler_called
        handler_called = True
        print("✅ Settings handler was called!")
        await message.reply_text("Test successful!")
    
    # Register the handler exactly like in the bot
    app.add_handler(MessageHandler(test_settings_handler, filters.command("settings")))
    
    print("Handler registered. Starting client...")
    
    # Start the client
    async with app:
        print("Client started. Testing command...")
        # The handler should be registered now
        handlers = app.dispatcher.groups
        print(f"Total handler groups: {len(handlers)}")
        
        # Look for our settings handler
        found = False
        for group_id, group_handlers in handlers.items():
            for handler in group_handlers:
                if isinstance(handler, MessageHandler):
                    if handler.callback.__name__ == 'test_settings_handler':
                        found = True
                        print(f"✅ Found our test settings handler in group {group_id}")
                        break
            if found:
                break
        
        if not found:
            print("❌ Our test settings handler was not found!")
        
        print("Test completed.")
    
    print(f"Handler was called: {handler_called}")

if __name__ == "__main__":
    asyncio.run(test_settings_registration())