# 🔄 Migration to WorkOS SSO

## What Changed?

Ghost Hire now uses **WorkOS SSO** instead of Google OAuth for authentication. WorkOS provides:

✅ **Better Enterprise Support**: SSO, SAML, OAuth all in one
✅ **Multiple Providers**: Google, Microsoft, GitHub, and more
✅ **Easier Setup**: One integration for all providers
✅ **Better Security**: Enterprise-grade authentication
✅ **Simpler Code**: No need for django-allauth

## Changes Made

### 1. Removed Dependencies
- ❌ `django-allauth`
- ❌ `PyJWT`
- ❌ `cryptography`
- ✅ Added `workos` (5.4.0)

### 2. Updated Configuration

**Old (.env):**
```env
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

**New (.env):**
```env
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/
```

### 3. New Files Created

- `haunted_profiles/workos_auth.py` - WorkOS authentication helper
- `haunted_profiles/auth_views.py` - Login and callback views

### 4. Removed Files

- `haunted_profiles/adapters.py` - No longer needed

### 5. Updated URLs

**Old:**
- `/accounts/google/login/` → Google OAuth
- `/accounts/google/login/callback/` → Callback

**New:**
- `/auth/login/` → WorkOS SSO
- `/auth/callback/` → Callback

## Setup Instructions

### 1. Install WorkOS SDK

```bash
pip install workos==5.4.0
```

### 2. Configure WorkOS Dashboard

1. Go to https://dashboard.workos.com/
2. Select your project
3. Navigate to **Configuration** → **Redirects**
4. Add these redirect URIs:
   - `http://localhost:8000/auth/callback/`
   - `http://127.0.0.1:8000/auth/callback/`
   - Add your production URL when deploying

### 3. Update Environment Variables

Update your `.env` with your WorkOS credentials:
```env
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=http://localhost:8000/auth/callback/
```

### 4. Run Migrations (if needed)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Test the Flow

1. Start server: `python manage.py runserver`
2. Go to: `http://localhost:8000`
3. Click "Rise from the Grave"
4. WorkOS will handle authentication
5. You'll be redirected back to the app

## How It Works

### Authentication Flow

```
1. User clicks "Rise from the Grave"
   ↓
2. Redirected to WorkOS hosted login
   ↓
3. User authenticates (Google, Microsoft, etc.)
   ↓
4. WorkOS redirects to /auth/callback/ with code
   ↓
5. App exchanges code for user profile
   ↓
6. User created/retrieved in database
   ↓
7. User logged in and redirected based on verification status
```

### User Creation

When a user logs in via WorkOS:

1. **WorkOS ID** is stored in `google_id` field (reusing existing field)
2. **Email** from WorkOS profile
3. **Username** auto-generated as `ghost_XXXXX`
4. User is created if doesn't exist
5. Existing users matched by WorkOS ID or email

## Benefits of WorkOS

### 1. Multiple Auth Providers
Users can sign in with:
- Google
- Microsoft
- GitHub
- Apple
- Any SAML provider

### 2. Enterprise Features
- SSO (Single Sign-On)
- SAML support
- Directory sync
- MFA enforcement

### 3. Simpler Code
- No complex OAuth flows
- No token management
- WorkOS handles everything

### 4. Better Security
- Enterprise-grade security
- Automatic token refresh
- Secure session management

## Testing

### Test with Different Providers

WorkOS supports multiple providers. To test:

1. Go to WorkOS Dashboard
2. Configure additional providers (Microsoft, GitHub, etc.)
3. Users can choose their preferred provider

### Test Locally

```bash
# Start server
python manage.py runserver

# Visit homepage
http://localhost:8000

# Click "Rise from the Grave"
# Authenticate with any configured provider
```

## Troubleshooting

### "Invalid redirect URI"
- Check WorkOS Dashboard → Redirects
- Make sure `http://localhost:8000/auth/callback/` is added
- Use exact URL (localhost vs 127.0.0.1)

### "Invalid client ID"
- Verify `WORKOS_CLIENT_ID` in `.env`
- Check it matches your WorkOS Dashboard

### "Authentication failed"
- Check WorkOS Dashboard logs
- Verify `WORKOS_API_KEY` is correct
- Make sure API key has proper permissions

### User not created
- Check Django logs
- Verify User model has `google_id` field
- Check database connection

## Production Deployment

### 1. Update Redirect URI

In `.env`:
```env
WORKOS_REDIRECT_URI=https://yourdomain.com/auth/callback/
```

### 2. Add to WorkOS Dashboard

Add production redirect URI:
```
https://yourdomain.com/auth/callback/
```

### 3. Use Production API Key

WorkOS provides separate keys for:
- Development: `sk_test_...`
- Production: `sk_live_...`

Update `.env` with production key.

## Migration Checklist

- [x] Install WorkOS SDK
- [x] Remove django-allauth
- [x] Update settings.py
- [x] Create WorkOS auth helpers
- [x] Update URLs
- [x] Update templates
- [x] Configure WorkOS Dashboard
- [x] Test authentication flow
- [x] Update documentation

## Need Help?

- **WorkOS Docs**: https://workos.com/docs
- **WorkOS Dashboard**: https://dashboard.workos.com/
- **Support**: support@workos.com

## 🎃 Happy Haunting with WorkOS!

Your Ghost Hire platform now has enterprise-grade authentication! 👻
