# 🔧 WorkOS SSO Troubleshooting Guide

## Issue: Can't Login with WorkOS

### Quick Fix Applied ✅

I've updated the code to use **WorkOS AuthKit** (User Management) instead of SSO. This is the correct approach for hosted authentication.

### What Changed:

**Before (Wrong):**
```python
workos.client.sso.get_authorization_url()  # ❌ For enterprise SSO only
workos.client.sso.get_profile_and_token()  # ❌ Wrong method
```

**After (Correct):**
```python
workos.client.user_management.get_authorization_url()  # ✅ For AuthKit
workos.client.user_management.authenticate_with_code()  # ✅ Correct method
```

## Steps to Fix Your WorkOS Setup

### 1. Check WorkOS Dashboard Configuration

Go to https://dashboard.workos.com/ and verify:

#### A. Enable AuthKit
1. Go to your project
2. Navigate to **Authentication** → **AuthKit**
3. Make sure AuthKit is **enabled**

#### B. Configure Redirect URI
1. Go to **Configuration** → **Redirects**
2. Add this exact URL:
   ```
   http://localhost:8000/auth/callback/
   ```
3. Click **Save**

#### C. Get Your Credentials
1. Go to **API Keys**
2. Copy your:
   - **Client ID**: Should start with `client_`
   - **API Key**: Should start with `sk_test_`

### 2. Update Your .env File

Make sure your `.env` has these exact values:

```env
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/
```

### 3. Restart Django Server

```bash
# Stop the server (Ctrl+C)
# Start it again
python manage.py runserver
```

### 4. Test the Login Flow

1. Go to: `http://localhost:8000`
2. Click **"Rise from the Grave"**
3. You should be redirected to WorkOS AuthKit login page
4. Sign in with your email
5. You'll be redirected back to the app

## Common Issues & Solutions

### Issue 1: "Invalid redirect URI"

**Error:** WorkOS says redirect URI doesn't match

**Solution:**
- Go to WorkOS Dashboard → Redirects
- Make sure you have: `http://localhost:8000/auth/callback/`
- Use exact URL (no trailing slash differences)
- Match http vs https

### Issue 2: "Invalid client ID"

**Error:** Authentication fails with client ID error

**Solution:**
- Check `.env` file has correct `WORKOS_CLIENT_ID`
- Should start with `client_`
- Copy from WorkOS Dashboard → API Keys

### Issue 3: "Invalid API key"

**Error:** Can't authenticate or get user info

**Solution:**
- Check `.env` file has correct `WORKOS_API_KEY`
- Should start with `sk_test_` (development) or `sk_live_` (production)
- Copy from WorkOS Dashboard → API Keys

### Issue 4: "Module not found: workos"

**Error:** Python can't find workos module

**Solution:**
```bash
pip install workos==5.4.0
```

### Issue 5: Database connection error

**Error:** MySQL access denied

**Solution:**
- Make sure you have `.env` file (not just `.env.example`)
- Check MySQL password in `.env` matches your MySQL root password
- Create database: `CREATE DATABASE ghost;`

### Issue 6: "No authentication methods configured"

**Error:** WorkOS says no auth methods available

**Solution:**
- Go to WorkOS Dashboard → Authentication
- Enable at least one provider:
  - Email/Password
  - Google
  - Microsoft
  - GitHub
  - etc.

## Testing Checklist

- [ ] `.env` file exists (not just `.env.example`)
- [ ] WorkOS Client ID is correct in `.env`
- [ ] WorkOS API Key is correct in `.env`
- [ ] Redirect URI added in WorkOS Dashboard
- [ ] AuthKit is enabled in WorkOS Dashboard
- [ ] At least one auth provider is enabled
- [ ] Django server is running
- [ ] MySQL database is created and accessible
- [ ] Migrations are run

## Debug Mode

To see detailed error messages, check Django logs:

```bash
python manage.py runserver
# Watch the console for errors when you try to login
```

Or check WorkOS Dashboard logs:
1. Go to WorkOS Dashboard
2. Navigate to **Logs**
3. See authentication attempts and errors

## Still Not Working?

### Check Django Logs

Look for errors in the console when you click "Rise from the Grave":

```python
# Common errors:
- "Invalid redirect_uri"
- "Invalid client_id"
- "Authentication failed"
```

### Check WorkOS Dashboard Logs

1. Go to https://dashboard.workos.com/
2. Click **Logs** in sidebar
3. Look for failed authentication attempts
4. Check error messages

### Verify Environment Variables Are Loading

Add this to `haunted_profiles/auth_views.py` temporarily:

```python
def workos_login(request):
    print(f"Client ID: {settings.WORKOS_CLIENT_ID}")
    print(f"API Key: {settings.WORKOS_API_KEY[:20]}...")
    print(f"Redirect URI: {settings.WORKOS_REDIRECT_URI}")
    # ... rest of code
```

Run server and check console output.

## Quick Test Command

```bash
# Test if WorkOS credentials are valid
python manage.py shell

>>> from django.conf import settings
>>> print(settings.WORKOS_CLIENT_ID)
>>> print(settings.WORKOS_API_KEY[:20])
>>> print(settings.WORKOS_REDIRECT_URI)
```

Should output your credentials without errors.

## Need More Help?

1. **WorkOS Docs**: https://workos.com/docs/user-management
2. **WorkOS Support**: support@workos.com
3. **WorkOS Dashboard**: https://dashboard.workos.com/

## 🎃 Once It Works

You should see:
1. Click "Rise from the Grave"
2. Redirect to WorkOS login page
3. Enter email/password or use social login
4. Redirect back to Ghost Hire
5. See verification page!

Happy Haunting! 👻
