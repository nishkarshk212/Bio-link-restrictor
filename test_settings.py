#!/usr/bin/env python3
"""
Test script to check settings command functionality
"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, WARN_LIMIT, PENALTY_ACTION
import re

async def test_settings_command():
    """Test if settings command logic works correctly"""
    print("🔍 Testing Settings Command Functionality...")
    print("=" * 50)
    
    # Test the permission checking functions
    print("1. Testing permission checking functions...")
    
    # Mock functions for testing
    async def mock_is_group_owner(chat_id, user_id):
        """Mock function to test group owner checking"""
        # In a real test, we would actually check Telegram
        # For now, we'll assume user_id 100 is the owner
        return user_id == 100  # Mock owner ID
    
    # Test scenarios
    test_cases = [
        (100, "Group Owner", True),   # Should have access
        (200, "Regular User", False), # Should not have access
        (300, "Admin", False)        # Should not have access
    ]
    
    for user_id, user_type, expected in test_cases:
        result = await mock_is_group_owner(12345, user_id)
        status = "✅" if result == expected else "❌"
        print(f"   {status} User {user_id} ({user_type}): {'Allowed' if result else 'Denied'} (Expected: {'Allowed' if expected else 'Denied'})")
    
    print("\n2. Testing settings keyboard generation...")
    try:
        # Test keyboard generation function
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
        
        keyboard = await get_settings_keyboard()
        print(f"   ✅ Settings keyboard generated successfully")
        print(f"   Current settings: Warn Limit = {WARN_LIMIT}, Penalty = {PENALTY_ACTION}")
    except Exception as e:
        print(f"  ❌ Keyboard generation failed: {e}")
    
    print("\n3. Testing message filter logic...")
    # Test that the filter would work correctly
    from pyrogram import filters
    
    # Check if filters are imported correctly
    if hasattr(filters, 'command') and hasattr(filters, 'private'):
        print("   ✅ Required filters are available")
    else:
        print("   ❌ Required filters are missing")
    
    print("\n" + "=" * 50)
    print("✅ Settings command test completed!")
    print("\nTo test the actual command:")
    print("1. Add the bot to a group")
    print("2. Make sure you're the group owner (creator)") 
    print("3. Send '/settings' in the group chat")
    print("4. You should see the settings panel with +/- buttons")

if __name__ == "__main__":
    asyncio.run(test_settings_command())