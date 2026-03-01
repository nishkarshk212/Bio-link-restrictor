#!/usr/bin/env python3
"""
Debug script to check if command handlers are registered correctly
"""
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import API_ID, API_HASH, BOT_TOKEN

async def debug_handlers():
    """Debug the registered handlers"""
    print("🔍 Debugging Command Handlers...")
    print("=" * 50)
    
    # Create a test client
    async with Client("debug_client", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as client:
        # Get all registered handlers
        handlers = client.dispatcher.groups
        
        print(f"Total handler groups: {len(handlers)}")
        
        # Look for command handlers
        command_handlers = []
        for group_id, group_handlers in handlers.items():
            print(f"\nGroup {group_id}:")
            for handler in group_handlers:
                if isinstance(handler, MessageHandler):
                    print(f"  - Handler: {handler.callback.__name__}")
                    if hasattr(handler.filters, 'commands'):
                        print(f"    Commands: {handler.filters.commands}")
                    if hasattr(handler.filters, 'group'):
                        print(f"    Group filter: {handler.filters.group}")
                    if hasattr(handler.filters, 'private'):
                        print(f"    Private filter: {handler.filters.private}")
                    
                    # Check if it's a settings command
                    if hasattr(handler.filters, 'commands') and 'settings' in handler.filters.commands:
                        command_handlers.append(handler)
        
        print(f"\nFound {len(command_handlers)} settings command handlers")
        
        if command_handlers:
            print("✅ Settings command is registered!")
            handler = command_handlers[0]
            print(f"Handler function: {handler.callback.__name__}")
            print("Filters:")
            print(f"  - Commands: {getattr(handler.filters, 'commands', 'None')}")
            print(f"  - Group: {getattr(handler.filters, 'group', 'None')}")
            print(f"  - Private: {getattr(handler.filters, 'private', 'None')}")
        else:
            print("❌ Settings command is NOT registered!")

if __name__ == "__main__":
    asyncio.run(debug_handlers())