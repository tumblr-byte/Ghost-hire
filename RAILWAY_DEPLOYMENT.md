# 🚂 Railway Deployment Guide for Ghost Hire

Complete guide to deploy Ghost Hire on Railway.app

---

## Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app/))
- Your code pushed to GitHub (without secrets!)

---

## Step 1: Prepare Your Repository

### 1.1 Clean Git History (Remove Secrets)

If you haven't already, run:

```cmd
.\clean-git-history.bat
```

This removes any secrets from your Git history.

### 1.2 Verify No Secrets in Code

Run the security check:

```cmd
.\check-secrets.bat
```

Make sure secrets are ONLY in `.env` (which is gitignored).

### 1.3 Push to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

---

## Step 2: Create Railway Project

### 2.1 Sign Up / Login

1. Go to [railway.app](https://railway.app/)
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your repositories

### 2.2 Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `Ghost-hire` repository
4. Railway will automatically detect it's a Django app

---

## Step 3: Add MySQL Database

### 3.1 Add Database Service

1. In your Railway project, click "New"
2. Select "Database"
3. Choose "Add MySQL"
4. Railway will provision a MySQL database

### 3.2 Note Database Credentials

Railway automatically creates these environment variables:
- `MYSQL_URL`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

---

## Step 4: Configure Environment Variables

### 4.1 Go to Variables Tab

1. Click on your web service (not the database)
2. Go to "Variables" tab
3. Add the following variables:

### 4.2 Required Environment Variables

```env
# Django Settings
SECRET_KEY=your-strong-secret-key-generate-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app

# Database (Railway provides these automatically, but you can override)
DB_NAME=${{MYSQL_DATABASE}}
DB_USER=${{MYSQL_USER}}
DB_PASSWORD=${{MYSQL_PASSWORD}}
DB_HOST=${{MYSQL_HOST}}
DB_PORT=${{MYSQL_PORT}}

# WorkOS Authentication
WORKOS_CLIENT_ID=client_your_client_id_here
WORKOS_API_KEY=sk_test_your_api_key_here
WORKOS_REDIRECT_URI=https://your-app-name.up.railway.app/auth/callback/

# SerpAPI
SERPAPI_KEY=your_serpapi_key_here
```

### 4.3 Generate Strong SECRET_KEY

```python
# Run this in Python to generate a new secret key
import secrets
print(secrets.token_urlsafe(50))
```

---

## Step 5: Configure Railway Settings

### 5.1 Create railway.json (Optional)

Create `railway.json` in your project root:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ghosthire.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 5.2 Create Procfile (Alternative)

Or create a `Procfile`:

```
web: python manage.py migrate && gunicorn ghosthire.wsgi:application --bind 0.0.0.0:$PORT
```

### 5.3 Update requirements.txt

Make sure `gunicorn` is in your `requirements.txt`:

```txt
Django==4.2.25
mysqlclient==2.2.7
Pillow==10.4.0
torch==2.7.1
torchvision==0.22.1
requests==2.32.4
python-dotenv==1.2.1
workos==5.4.0
beautifulsoup4==4.12.3
gunicorn==21.2.0
```

---

## Step 6: Update Django Settings for Production

### 6.1 Update settings.py

Make sure your `ghosthire/settings.py` has:

```python
import os
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', os.environ.get('MYSQL_DATABASE', 'ghost')),
        'USER': os.environ.get('DB_USER', os.environ.get('MYSQL_USER', 'root')),
        'PASSWORD': os.environ.get('DB_PASSWORD', os.environ.get('MYSQL_PASSWORD', '')),
        'HOST': os.environ.get('DB_HOST', os.environ.get('MYSQL_HOST', 'localhost')),
        'PORT': os.environ.get('DB_PORT', os.environ.get('MYSQL_PORT', '3306')),
    }
}

# Static files (important for Railway)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

---

## Step 7: Update WorkOS Redirect URI

### 7.1 Get Your Railway URL

After deployment, Railway will give you a URL like:
```
https://your-app-name.up.railway.app
```

### 7.2 Update WorkOS Dashboard

1. Go to [WorkOS Dashboard](https://dashboard.workos.com/)
2. Navigate to **Configuration** → **Redirects**
3. Add your Railway URL:
   ```
   https://your-app-name.up.railway.app/auth/callback/
   ```

### 7.3 Update Environment Variable

In Railway, update:
```env
WORKOS_REDIRECT_URI=https://your-app-name.up.railway.app/auth/callback/
```

---

## Step 8: Deploy!

### 8.1 Push Changes

```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

### 8.2 Railway Auto-Deploy

Railway will automatically:
1. Detect the push
2. Build your application
3. Run migrations
4. Collect static files
5. Start the server

### 8.3 Monitor Deployment

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Watch the build logs

---

## Step 9: Post-Deployment

### 9.1 Create Superuser

Use Railway CLI or run command in Railway:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run command
railway run python manage.py createsuperuser
```

### 9.2 Test Your Application

1. Visit your Railway URL
2. Click "Rise from the Grave"
3. Test WorkOS authentication
4. Upload verification photo
5. Create ghost profile

---

## Troubleshooting

### Issue 1: Build Fails

**Error**: `mysqlclient` installation fails

**Solution**: Railway should handle this automatically with Nixpacks. If not, create `nixpacks.toml`:

```toml
[phases.setup]
aptPkgs = ['default-libmysqlclient-dev', 'pkg-config']
```

### Issue 2: Database Connection Error

**Error**: Can't connect to MySQL

**Solution**:
- Check that MySQL service is running in Railway
- Verify environment variables are set correctly
- Make sure web service and database are in the same project

### Issue 3: Static Files Not Loading

**Error**: CSS/JS not loading

**Solution**:
- Make sure `collectstatic` runs in start command
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Verify Railway is serving static files

### Issue 4: WorkOS Authentication Fails

**Error**: Redirect URI mismatch

**Solution**:
- Update WorkOS Dashboard with Railway URL
- Update `WORKOS_REDIRECT_URI` environment variable
- Make sure URL includes `https://` and `/auth/callback/`

### Issue 5: Application Crashes

**Error**: Application keeps restarting

**Solution**:
- Check Railway logs: Click service → "Logs" tab
- Look for Python errors
- Verify all environment variables are set
- Check database connection

---

## Railway CLI Commands

### Install CLI

```bash
npm i -g @railway/cli
```

### Useful Commands

```bash
# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run Django commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell

# Open in browser
railway open
```

---

## Cost Estimation

Railway offers:
- **Free Tier**: $5 credit/month (good for testing)
- **Hobby Plan**: $5/month + usage
- **Pro Plan**: $20/month + usage

Typical Ghost Hire usage:
- Web service: ~$3-5/month
- MySQL database: ~$2-3/month
- **Total**: ~$5-8/month

---

## Environment Variables Checklist

- [ ] `SECRET_KEY` - Strong, unique key
- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - Your Railway domain
- [ ] `DB_NAME` - From Railway MySQL
- [ ] `DB_USER` - From Railway MySQL
- [ ] `DB_PASSWORD` - From Railway MySQL
- [ ] `DB_HOST` - From Railway MySQL
- [ ] `DB_PORT` - From Railway MySQL
- [ ] `WORKOS_CLIENT_ID` - From WorkOS Dashboard
- [ ] `WORKOS_API_KEY` - From WorkOS Dashboard
- [ ] `WORKOS_REDIRECT_URI` - Your Railway URL + `/auth/callback/`
- [ ] `SERPAPI_KEY` - From SerpAPI

---

## Security Best Practices

1. **Never commit secrets** - Use Railway environment variables
2. **Use strong SECRET_KEY** - Generate new one for production
3. **Enable HTTPS** - Railway provides this automatically
4. **Set DEBUG=False** - Never run debug mode in production
5. **Rotate API keys** - Change keys regularly
6. **Monitor logs** - Check Railway logs for suspicious activity
7. **Backup database** - Railway provides automatic backups

---

## Updating Your Application

### Deploy New Changes

```bash
# Make changes to your code
git add .
git commit -m "Your changes"
git push origin main
```

Railway will automatically redeploy!

### Rollback

If something goes wrong:
1. Go to Railway dashboard
2. Click "Deployments"
3. Find previous working deployment
4. Click "Redeploy"

---

## Custom Domain (Optional)

### Add Your Own Domain

1. Go to Railway project
2. Click on your service
3. Go to "Settings" tab
4. Scroll to "Domains"
5. Click "Add Domain"
6. Enter your domain
7. Update DNS records as instructed
8. Update `ALLOWED_HOSTS` and `WORKOS_REDIRECT_URI`

---

## Support

- **Railway Docs**: https://docs.railway.app/
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app/

---

## 🎃 Happy Deploying!

Your Ghost Hire platform is now live on Railway! 👻

**Need help?** Check Railway logs or open an issue on GitHub.
