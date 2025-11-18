# 📋 WorkOS Dashboard Setup - Step by Step

## 🎯 Goal: Add Redirect URI to WorkOS

Your redirect URI: `http://localhost:8000/auth/callback/`

## 📍 Where to Find It in WorkOS Dashboard

### Method 1: SSO Configuration (If using Google OAuth)

```
WorkOS Dashboard
    └── SSO (left sidebar)
        └── Configuration
            └── Redirect URIs
                └── [Add Redirect URI button]
                    └── Enter: http://localhost:8000/auth/callback/
                    └── Click Save
```

### Method 2: Authentication Configuration (If using Email/Password)

```
WorkOS Dashboard
    └── Authentication (left sidebar)
        └── Configuration
            └── Redirect URIs
                └── [Add Redirect URI button]
                    └── Enter: http://localhost:8000/auth/callback/
                    └── Click Save
```

## 🔍 Visual Steps

### Step 1: Login to WorkOS
```
https://dashboard.workos.com/
```

### Step 2: Select Your Project
```
┌─────────────────────────────────┐
│  My Projects                    │
│  ┌───────────────────────────┐  │
│  │ Your Project Name         │  │ ← Click this
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Step 3: Go to Configuration
```
Left Sidebar:
┌─────────────────┐
│ Dashboard       │
│ SSO             │ ← Click here
│ Authentication  │    OR here
│ API Keys        │
│ Logs            │
└─────────────────┘
```

### Step 4: Find Redirect URIs Section
```
Configuration Page:
┌──────────────────────────────────────┐
│ Configuration                        │
│                                      │
│ Redirect URIs                        │
│ ┌──────────────────────────────────┐ │
│ │ [Add Redirect URI]               │ │ ← Click this
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

### Step 5: Add Your URI
```
Add Redirect URI Dialog:
┌──────────────────────────────────────┐
│ Add Redirect URI                     │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ http://localhost:8000/auth/      │ │ ← Type this
│ │ callback/                        │ │
│ └──────────────────────────────────┘ │
│                                      │
│ [Cancel]  [Save]                     │ ← Click Save
└──────────────────────────────────────┘
```

### Step 6: Verify It's Added
```
Redirect URIs:
┌──────────────────────────────────────┐
│ http://localhost:8000/auth/callback/ │ ✅
│ [Delete]                             │
└──────────────────────────────────────┘
```

## ⚠️ Common Mistakes

### ❌ Wrong:
- `http://localhost:8000/auth/callback` (missing trailing slash)
- `https://localhost:8000/auth/callback/` (https instead of http)
- `http://localhost:8000/callback/` (missing /auth/)
- `http://localhost:3000/auth/callback/` (wrong port)

### ✅ Correct:
- `http://localhost:8000/auth/callback/`

## 🔄 After Adding

1. **Save** in WorkOS Dashboard
2. **Wait** 10-30 seconds
3. **Restart** Django server:
   ```bash
   python manage.py runserver
   ```
4. **Test** the login

## 🧪 Test It

```bash
# Run test script
python test_workos.py

# Should show:
✅ Authorization URL generated successfully!
```

Then test in browser:
```
1. Go to: http://localhost:8000
2. Click: "Rise from the Grave"
3. Should redirect to WorkOS (not show error)
```

## 📞 Still Not Working?

### Check WorkOS Logs

1. Go to WorkOS Dashboard
2. Click **Logs** in left sidebar
3. Look for recent authentication attempts
4. Check error messages

### Check Your Environment

Run this in terminal:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Redirect URI:', os.getenv('WORKOS_REDIRECT_URI'))"
```

Should output:
```
Redirect URI: http://localhost:8000/auth/callback/
```

### Check Django Settings

Run this:
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.WORKOS_REDIRECT_URI)
http://localhost:8000/auth/callback/
```

## 🎃 Success Looks Like

When it works, you'll see:
1. Click "Rise from the Grave"
2. Redirect to WorkOS login page
3. See Google sign-in button (or email/password form)
4. Sign in
5. Redirect back to Ghost Hire
6. See verification page!

You're almost there! 👻
