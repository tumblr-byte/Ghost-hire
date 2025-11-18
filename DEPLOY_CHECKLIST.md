# 🚀 Railway Deployment Checklist

Quick checklist before deploying to Railway.

---

## Pre-Deployment

### 1. Clean Repository
- [ ] Run `.\check-secrets.bat` to verify no secrets in code
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Ensure `.env.example` has placeholder values only
- [ ] Run `.\clean-git-history.bat` if needed to remove secrets from Git history

### 2. Code Ready
- [ ] All changes committed
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes `gunicorn`
- [ ] `Procfile` exists
- [ ] `railway.json` exists
- [ ] `nixpacks.toml` exists

### 3. Configuration Files
- [ ] `settings.py` uses environment variables for database
- [ ] `settings.py` has production security settings
- [ ] Static files configured (`STATIC_ROOT`, `STATIC_URL`)
- [ ] Media files configured (`MEDIA_ROOT`, `MEDIA_URL`)

---

## Railway Setup

### 4. Create Project
- [ ] Sign up/login to Railway
- [ ] Create new project from GitHub repo
- [ ] Add MySQL database service

### 5. Environment Variables
Set these in Railway dashboard:

- [ ] `SECRET_KEY` - Generate new strong key
- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - Your Railway domain
- [ ] `WORKOS_CLIENT_ID` - From WorkOS Dashboard
- [ ] `WORKOS_API_KEY` - From WorkOS Dashboard
- [ ] `WORKOS_REDIRECT_URI` - `https://your-app.up.railway.app/auth/callback/`
- [ ] `SERPAPI_KEY` - From SerpAPI

Database variables (Railway auto-provides):
- [ ] `MYSQL_DATABASE`
- [ ] `MYSQL_USER`
- [ ] `MYSQL_PASSWORD`
- [ ] `MYSQL_HOST`
- [ ] `MYSQL_PORT`

---

## WorkOS Configuration

### 6. Update WorkOS Dashboard
- [ ] Go to WorkOS Dashboard
- [ ] Add Railway URL to Redirects: `https://your-app.up.railway.app/auth/callback/`
- [ ] Verify AuthKit is enabled
- [ ] Test authentication provider is configured

---

## Deployment

### 7. Deploy
- [ ] Push code to GitHub
- [ ] Railway auto-deploys
- [ ] Monitor build logs in Railway dashboard
- [ ] Check for errors

### 8. Post-Deployment
- [ ] Create superuser: `railway run python manage.py createsuperuser`
- [ ] Visit your Railway URL
- [ ] Test "Rise from the Grave" button
- [ ] Test WorkOS authentication
- [ ] Upload test verification photo
- [ ] Create test ghost profile
- [ ] Check static files load correctly
- [ ] Check media files upload correctly

---

## Testing

### 9. Functionality Tests
- [ ] Homepage loads
- [ ] Authentication works
- [ ] Photo upload works
- [ ] Profile creation works
- [ ] Portfolio display works
- [ ] All pages accessible
- [ ] No console errors

### 10. Security Tests
- [ ] HTTPS enabled (Railway provides this)
- [ ] Debug mode is OFF
- [ ] Verification photos not publicly accessible
- [ ] Environment variables not exposed
- [ ] No secrets in code

---

## Troubleshooting

If something goes wrong:

1. **Check Railway Logs**
   - Go to Railway dashboard
   - Click your service
   - View "Logs" tab

2. **Common Issues**
   - Database connection: Check MySQL service is running
   - Static files: Verify `collectstatic` runs in start command
   - WorkOS auth: Check redirect URI matches exactly
   - Build fails: Check `nixpacks.toml` has required packages

3. **Rollback**
   - Go to "Deployments" tab
   - Find previous working deployment
   - Click "Redeploy"

---

## Generate SECRET_KEY

Run this in Python:

```python
import secrets
print(secrets.token_urlsafe(50))
```

Copy the output and use it as your `SECRET_KEY` in Railway.

---

## Quick Commands

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run Django commands
railway run python manage.py createsuperuser
railway run python manage.py migrate
railway run python manage.py shell
```

---

## 🎃 Ready to Deploy!

Once all checkboxes are checked, you're ready to go live! 👻

**Need help?** See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions.
