#!/usr/bin/env python3
"""
Test script to verify Telegram API connection
"""

import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

async def test_connection():
    """Test the Telegram API connection"""
    print("🔍 Testing Telegram API Connection...")
    print("=" * 50)
    
    # Test bot connection
    print("🤖 Testing Bot Connection...")
    try:
        async with Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as bot:
            me = await bot.get_me()
            print(f"✅ Bot connected successfully!")
            print(f"   Bot Name: {me.first_name}")
            print(f"   Bot Username: @{me.username}")
            print(f"   Bot ID: {me.id}")
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All connections successful!")
    return True

if __name__ == "__main__":
    asyncio.run(test_connection())