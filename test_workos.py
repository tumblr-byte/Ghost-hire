#!/usr/bin/env python
"""
Quick test script to verify WorkOS configuration
Run: python test_workos.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 Testing WorkOS Configuration")
print("=" * 60)

# Check if .env file exists
if not os.path.exists('.env'):
    print("❌ ERROR: .env file not found!")
    print("   Create it by copying .env.example:")
    print("   copy .env.example .env")
    exit(1)
else:
    print("✅ .env file found")

# Check environment variables
client_id = os.environ.get('WORKOS_CLIENT_ID')
api_key = os.environ.get('WORKOS_API_KEY')
redirect_uri = os.environ.get('WORKOS_REDIRECT_URI')

print("\n📋 Environment Variables:")
print("-" * 60)

if client_id:
    print(f"✅ WORKOS_CLIENT_ID: {client_id}")
else:
    print("❌ WORKOS_CLIENT_ID: Not set!")

if api_key:
    print(f"✅ WORKOS_API_KEY: {api_key[:20]}... (hidden)")
else:
    print("❌ WORKOS_API_KEY: Not set!")

if redirect_uri:
    print(f"✅ WORKOS_REDIRECT_URI: {redirect_uri}")
else:
    print("❌ WORKOS_REDIRECT_URI: Not set!")

# Test WorkOS SDK
print("\n🔧 Testing WorkOS SDK:")
print("-" * 60)

try:
    import workos
    print("✅ WorkOS SDK installed")
    
    # Configure WorkOS
    workos.api_key = api_key
    workos.client_id = client_id
    
    print("✅ WorkOS configured")
    
    # Try to get authorization URL
    try:
        from workos import WorkOSClient
        client = WorkOSClient(api_key=api_key, client_id=client_id)
        auth_url = client.sso.get_authorization_url(
            provider='GoogleOAuth',
            redirect_uri=redirect_uri,
            state='test',
        )
        print("✅ Authorization URL generated successfully!")
        print(f"   URL: {auth_url[:80]}...")
        
    except Exception as e:
        print(f"❌ Error generating authorization URL: {e}")
        print("\n💡 Possible issues:")
        print("   - Check your Client ID is correct")
        print("   - Check your API Key is correct")
        print("   - Make sure AuthKit is enabled in WorkOS Dashboard")
        
except ImportError:
    print("❌ WorkOS SDK not installed!")
    print("   Install it: pip install workos==5.4.0")

# Check database configuration
print("\n💾 Database Configuration:")
print("-" * 60)

db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

if db_name:
    print(f"✅ DB_NAME: {db_name}")
else:
    print("❌ DB_NAME: Not set!")

if db_user:
    print(f"✅ DB_USER: {db_user}")
else:
    print("❌ DB_USER: Not set!")

if db_password:
    print(f"✅ DB_PASSWORD: {'*' * len(db_password)} (hidden)")
else:
    print("❌ DB_PASSWORD: Not set!")

# Summary
print("\n" + "=" * 60)
print("📊 Summary")
print("=" * 60)

all_good = all([client_id, api_key, redirect_uri, db_name, db_user, db_password])

if all_good:
    print("✅ All configuration looks good!")
    print("\n🚀 Next steps:")
    print("   1. Make sure MySQL is running")
    print("   2. Create database: CREATE DATABASE ghost;")
    print("   3. Run migrations: python manage.py migrate")
    print("   4. Start server: python manage.py runserver")
    print("   5. Visit: http://localhost:8000")
else:
    print("❌ Some configuration is missing!")
    print("\n💡 Fix the issues above and try again")

print("=" * 60)
