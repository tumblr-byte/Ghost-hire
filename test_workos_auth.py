#!/usr/bin/env python
"""
Test WorkOS Authentication
"""
import os
from dotenv import load_dotenv
from workos import WorkOSClient

load_dotenv()

print("=" * 60)
print("🔍 Testing WorkOS Authentication")
print("=" * 60)

# Get credentials
client_id = os.environ.get('WORKOS_CLIENT_ID')
api_key = os.environ.get('WORKOS_API_KEY')
redirect_uri = os.environ.get('WORKOS_REDIRECT_URI')

print(f"\n✅ Client ID: {client_id}")
print(f"✅ API Key: {api_key[:20]}...")
print(f"✅ Redirect URI: {redirect_uri}")

# Initialize WorkOS client
try:
    workos_client = WorkOSClient(
        api_key=api_key,
        client_id=client_id,
    )
    print("\n✅ WorkOS Client initialized")
    
    # Try to get authorization URL
    try:
        auth_url = workos_client.sso.get_authorization_url(
            provider='GoogleOAuth',
            redirect_uri=redirect_uri,
            state='test',
        )
        print(f"\n✅ Authorization URL generated!")
        print(f"URL: {auth_url}")
        print("\n🎉 WorkOS is configured correctly!")
        print("\nNext: Try this URL in your browser to test Google login")
        
    except Exception as e:
        print(f"\n❌ Error generating auth URL: {e}")
        print("\n💡 This might be the issue!")
        
except Exception as e:
    print(f"\n❌ Error initializing WorkOS: {e}")

print("=" * 60)
