# 🚀 Final Setup Steps - You're Almost There!

## ✅ What's Working Now

- WorkOS SDK is configured correctly
- Environment variables are loaded
- Authorization URL generation works
- Database credentials are set

## 🔧 What You Need to Do

### Step 1: Create MySQL Database

Open MySQL command line:
```bash
mysql -u root -p
```

Enter your password: `Moon90child@`

Then run:
```sql
CREATE DATABASE ghost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Step 2: Configure Google OAuth in WorkOS

1. Go to https://dashboard.workos.com/
2. Select your project
3. Navigate to **SSO** → **Configuration**
4. Click **Add Connection**
5. Select **Google OAuth**
6. Follow the setup wizard

**OR** if you want to use WorkOS's built-in auth:
1. Go to **Authentication** in WorkOS Dashboard
2. Enable **Email/Password** authentication
3. This allows users to sign up with email directly

### Step 3: Run Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter:
- Email: your@email.com
- Username: admin
- Password: (your choice)

### Step 5: Start the Server

```bash
python manage.py runserver
```

### Step 6: Test It!

1. Open browser: `http://localhost:8000`
2. Click **"Rise from the Grave"**
3. You'll be redirected to WorkOS
4. Sign in with Google (or email if you enabled it)
5. You'll be redirected back to Ghost Hire!

## 🎃 You're Done!

Your Ghost Hire platform is ready to haunt! 👻

## Troubleshooting

### If login still doesn't work:

1. **Check WorkOS Dashboard Logs:**
   - Go to https://dashboard.workos.com/
   - Click **Logs**
   - See what errors are happening

2. **Make sure redirect URI is added:**
   - WorkOS Dashboard → **Redirects**
   - Add: `http://localhost:8000/auth/callback/`

3. **Enable at least one auth method:**
   - WorkOS Dashboard → **Authentication**
   - Enable Email/Password OR
   - Configure Google OAuth in SSO section

Happy Haunting! 🎃👻
