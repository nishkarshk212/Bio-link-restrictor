#!/usr/bin/env python3
"""
Test script to verify link detection functionality
"""

import re
from config import LINK_PATTERNS

def test_link_detection():
    """Test the link detection patterns"""
    
    # Compile patterns
    link_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in LINK_PATTERNS]
    
    def has_links_in_bio(bio_text):
        """Check if the bio contains any links"""
        if not bio_text:
            return False
        
        bio_lower = bio_text.lower()
        for pattern in link_patterns:
            if pattern.search(bio_lower):
                return True
        return False
    
    # Test cases
    test_cases = [
        ("", False, "Empty bio"),
        ("Just a regular bio without links", False, "No links"),
        ("Check out my website: https://example.com", True, "HTTPS link"),
        ("Visit http://test.com for more info", True, "HTTP link"),
        ("My Telegram: t.me/username", True, "Telegram link"),
        ("Website: www.example.com", True, "WWW link"),
        ("Join here: telegram.me/group", True, "Telegram.me link"),
        ("Short link: bit.ly/abc123", True, "Bit.ly link"),
        ("Tiny url: tinyurl.com/xyz", True, "TinyURL link"),
        ("Regular text with no links at all", False, "No links 2"),
        ("Contact me via email: user@example.com", False, "Email (not a link)"),
        ("My bio t.me/", True, "Partial Telegram link"),
    ]
    
    print("🧪 Testing Link Detection")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for bio, expected, description in test_cases:
        result = has_links_in_bio(bio)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        print(f"{status} | {description}")
        print(f"      Bio: '{bio}'")
        print(f"      Expected: {expected}, Got: {result}")
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {failed} tests failed. Check the patterns in config.py")

if __name__ == "__main__":
    test_link_detection()