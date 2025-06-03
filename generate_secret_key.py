#!/usr/bin/env python3
"""
Generate a secure Django secret key for production use.
Run this script and copy the output to your .env file.
"""

from django.core.management.utils import get_random_secret_key

if __name__ == "__main__":
    secret_key = get_random_secret_key()
    print("🔑 Generated Django Secret Key:")
    print("-" * 50)
    print(secret_key)
    print("-" * 50)
    print("📝 Add this to your .env file:")
    print(f"SECRET_KEY={secret_key}")
    print("\n⚠️  Keep this secret and never commit it to version control!") 