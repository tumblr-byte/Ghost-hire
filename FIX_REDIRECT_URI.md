# 🔧 Fix "Invalid Redirect URI" Error

## The Problem

WorkOS is rejecting the redirect because the URI in your code doesn't match what's configured in your WorkOS Dashboard.

## The Solution - Add Redirect URI to WorkOS Dashboard

### Step 1: Go to WorkOS Dashboard

1. Open: https://dashboard.workos.com/
2. Log in to your account
3. Select your project

### Step 2: Add Redirect URI

#### Option A: If using SSO (Google OAuth)

1. Click **SSO** in the left sidebar
2. Click **Configuration**
3. Find **Redirect URIs** section
4. Click **Add Redirect URI**
5. Enter EXACTLY: `http://localhost:8000/auth/callback/`
6. Click **Save**

#### Option B: If using Authentication (Email/Password)

1. Click **Authentication** in the left sidebar
2. Click **Configuration**
3. Find **Redirect URIs** section
4. Click **Add Redirect URI**
5. Enter EXACTLY: `http://localhost:8000/auth/callback/`
6. Click **Save**

### Step 3: Important - Check for Trailing Slash

Make sure you include the trailing slash `/` at the end:
- ✅ CORRECT: `http://localhost:8000/auth/callback/`
- ❌ WRONG: `http://localhost:8000/auth/callback`

### Step 4: Also Add Without Trailing Slash (Just in Case)

Some systems are picky, so add both:
1. `http://localhost:8000/auth/callback/` (with slash)
2. `http://localhost:8000/auth/callback` (without slash)

### Step 5: Add 127.0.0.1 Version Too

Also add:
1. `http://127.0.0.1:8000/auth/callback/`
2. `http://127.0.0.1:8000/auth/callback`

This covers both localhost and 127.0.0.1.

## Quick Visual Guide

Your WorkOS Dashboard should look like this:

```
Redirect URIs:
┌─────────────────────────────────────────────┐
│ http://localhost:8000/auth/callback/        │ ✅
│ http://localhost:8000/auth/callback         │ ✅
│ http://127.0.0.1:8000/auth/callback/        │ ✅
│ http://127.0.0.1:8000/auth/callback         │ ✅
└─────────────────────────────────────────────┘
```

## After Adding Redirect URIs

1. **Save** the changes in WorkOS Dashboard
2. **Wait** 10-30 seconds for changes to propagate
3. **Restart** your Django server:
   ```bash
   # Press Ctrl+C to stop
   python manage.py runserver
   ```
4. **Test** again:
   - Go to `http://localhost:8000`
   - Click "Rise from the Grave"
   - Should work now! 🎃

## Still Getting Error?

### Check These:

1. **Exact Match**: The URI must match EXACTLY (including http vs https, trailing slash, etc.)

2. **Check Your Browser URL**: When you get the error, look at the browser URL. It might show what redirect URI WorkOS is expecting.

3. **Check WorkOS Logs**:
   - Go to WorkOS Dashboard
   - Click **Logs** in sidebar
   - Look for the failed authentication attempt
   - It will show what redirect URI was used

4. **Environment Variable**: Make sure your `.env` file has:
   ```env
   WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/
   ```

5. **Restart Server**: After changing `.env`, always restart Django:
   ```bash
   python manage.py runserver
   ```

## Alternative: Use WorkOS Environment

If you're still having issues, you might be using the wrong WorkOS environment:

1. Go to WorkOS Dashboard
2. Check if you're in **Development** or **Production** environment
3. Make sure you're using the correct:
   - Client ID (starts with `client_`)
   - API Key (starts with `sk_test_` for dev or `sk_live_` for prod)

## Test Command

Run this to verify your configuration:

```bash
python test_workos.py
```

Should show:
```
✅ WORKOS_REDIRECT_URI: http://localhost:8000/auth/callback/
✅ Authorization URL generated successfully!
```

## 🎃 Once It Works

You should see:
1. Click "Rise from the Grave"
2. Redirect to WorkOS login page (not error page)
3. Sign in with Google
4. Redirect back to Ghost Hire verification page

Happy Haunting! 👻
