#!/usr/bin/env python3
"""
Test production settings locally before deployment.
This script checks if all production configurations are working.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

def test_production_settings():
    """Test production settings configuration."""
    
    print("🧪 Testing Production Settings")
    print("=" * 50)
    
    # Test environment variables
    required_vars = ['SECRET_KEY', 'WEATHER_API_KEY', 'WEATHER_STATION_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Create a .env file with required variables")
        return False
    else:
        print("✅ All required environment variables are set")
    
    # Test DEBUG setting
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    if debug:
        print("⚠️  DEBUG is True - set DEBUG=False for production")
    else:
        print("✅ DEBUG is False (production mode)")
    
    # Test SECRET_KEY
    secret_key = os.environ.get('SECRET_KEY', '')
    if 'django-insecure' in secret_key:
        print("❌ Using insecure default SECRET_KEY")
        print("   Generate a new one with: python generate_secret_key.py")
        return False
    else:
        print("✅ SECRET_KEY looks secure")
    
    print("\n🔧 Django Settings Check")
    print("-" * 30)
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_station.settings')
        django.setup()
        
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DATABASE: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
        
        # Test weather service
        from weather.services import WeatherService
        weather_service = WeatherService()
        print("✅ Weather service initialized successfully")
        
        print("\n🎉 Production settings test passed!")
        print("   Your app is ready for deployment!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Django settings: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, skipping .env file loading")
    
    success = test_production_settings()
    sys.exit(0 if success else 1) 