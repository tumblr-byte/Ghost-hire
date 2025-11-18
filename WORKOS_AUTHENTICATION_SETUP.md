# 🎯 WorkOS Authentication Setup Guide

## What You're Seeing

You found the **Authentication** section in WorkOS Dashboard which shows:
- Google OAuth
- GitHub OAuth  
- Other providers

This is the RIGHT place! ✅

## Quick Setup (2 Options)

### Option 1: Demo Mode (Fastest - For Testing) ⚡

1. In WorkOS Dashboard → **Authentication**
2. Click **Google OAuth**
3. Click **"Enable Demo credentials"**
4. Click **Save**
5. Done! Test it now.

**Pros:**
- Works immediately
- No Google setup needed
- Perfect for testing

**Cons:**
- Demo only (not for production)
- Limited to test accounts

### Option 2: Your Own Google OAuth (Production) 🔧

If you want to use your own Google credentials:

#### Step 1: Get Google OAuth Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Add Authorized redirect URI:
   ```
   https://auth.workos.com/sso/oauth/google/GO0HIrT1tHRAKr8sRTSA1U83t/callback
   ```
   (Copy this from your WorkOS Dashboard - it's shown on the Google OAuth page)

7. Click **Create**
8. Copy your:
   - Client ID
   - Client Secret

#### Step 2: Add to WorkOS

1. Go back to WorkOS Dashboard → **Authentication** → **Google OAuth**
2. Paste your **Google Client ID**
3. Paste your **Google Client Secret**
4. Click **Save**

## Important: Add Your App's Redirect URI

After enabling Google (demo or your own), you MUST add your app's redirect URI:

1. In WorkOS Dashboard → **Authentication**
2. Scroll down to **Redirect URIs** section
3. Click **Add Redirect URI**
4. Enter: `http://localhost:8000/auth/callback/`
5. Click **Save**

Also add these for safety:
- `http://localhost:8000/auth/callback`
- `http://127.0.0.1:8000/auth/callback/`
- `http://127.0.0.1:8000/auth/callback`

## Code Changes Made ✅

I've updated the code to use WorkOS **User Management API** instead of SSO. This works with the Authentication section you're seeing.

The new code:
- Uses `https://api.workos.com/user_management/authorize` for login
- Uses `https://api.workos.com/user_management/authenticate` for callback
- Works with Google OAuth (demo or your own)

## Test It Now!

1. **Enable Demo Credentials** (or add your own Google OAuth)
2. **Add Redirect URI**: `http://localhost:8000/auth/callback/`
3. **Restart Django**:
   ```bash
   python manage.py runserver
   ```
4. **Test**:
   - Go to `http://localhost:8000`
   - Click "Rise from the Grave"
   - Should redirect to WorkOS login
   - Sign in with Google
   - Redirect back to Ghost Hire! 🎃

## Troubleshooting

### "Invalid redirect URI" error

Make sure you added `http://localhost:8000/auth/callback/` in:
- WorkOS Dashboard → Authentication → Redirect URIs

### "No authentication methods configured"

Make sure you:
- Enabled Google OAuth (demo or your own)
- Clicked Save

### Still not working?

Check WorkOS Dashboard → **Logs** to see what's happening.

## What About GitHub, Microsoft, etc.?

You can enable multiple providers:
1. Go to WorkOS Dashboard → **Authentication**
2. Click on any provider (GitHub, Microsoft, etc.)
3. Enable demo credentials or add your own
4. Users can choose which one to use!

## 🎃 Success!

When it works:
1. Click "Rise from the Grave"
2. See WorkOS login page
3. Click "Sign in with Google"
4. Authenticate
5. Redirect to Ghost Hire verification page!

You're almost there! 👻
