# 📤 Step-by-Step Guide: Update GitHub for Railway Deployment

## Step 1: Check Git Status

```cmd
git status
```

This shows what files have changed.

---

## Step 2: Remove Siamese Model from Git (if it was committed)

### Check if model is in Git:
```cmd
git ls-files | findstr "best_siamese_model.pth"
```

### If it shows up, remove it from Git:
```cmd
git rm --cached best_siamese_model.pth
```

### Make sure it's in .gitignore:
```cmd
echo best_siamese_model.pth >> .gitignore
echo *.pth >> .gitignore
echo *.pt >> .gitignore
```

---

## Step 3: Add All Changes

```cmd
git add .
```

This stages all your changes (removed PyTorch, updated flow, new docs).

---

## Step 4: Commit Changes

```cmd
git commit -m "Optimize for Railway deployment - remove PyTorch, skip verification"
```

---

## Step 5: Push to GitHub

```cmd
git push origin main
```

If you get an error about diverged branches, use:
```cmd
git push origin main --force
```

⚠️ **Warning**: `--force` will overwrite remote history. Only use if you're sure!

---

## Step 6: Verify on GitHub

1. Go to your GitHub repo: https://github.com/tumblr-byte/Ghost-hire
2. Check that:
   - ✅ `requirements.txt` doesn't have `torch` or `torchvision`
   - ✅ `best_siamese_model.pth` is NOT in the repo
   - ✅ New files are there: `README_SIAMESE.md`, `DEPLOYMENT_NOTES.md`
   - ✅ `haunted_profiles/auth_views.py` has auto-verify code

---

## Step 7: Clean Up Local Files (Optional)

If you want to keep your local setup with PyTorch for demo:

### Create a separate requirements file for local:
```cmd
copy requirements.txt requirements-local.txt
```

### Edit requirements-local.txt and add back:
```
torch==2.7.1
torchvision==0.22.1
```

### To switch between local and Railway:

**For Local (with PyTorch):**
```cmd
pip install -r requirements-local.txt
```

**For Railway (without PyTorch):**
```cmd
pip install -r requirements.txt
```

---

## Troubleshooting

### Issue 1: "Model file too large to push"

**Error**: `remote: error: File best_siamese_model.pth is 500MB; this exceeds GitHub's file size limit`

**Solution**:
```cmd
# Remove from Git history
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch best_siamese_model.pth" --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin main --force
```

### Issue 2: "Push rejected - diverged branches"

**Error**: `! [rejected] main -> main (non-fast-forward)`

**Solution**:
```cmd
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

Or force push (if you're sure):
```cmd
git push origin main --force
```

### Issue 3: "Still seeing old files on GitHub"

**Solution**:
```cmd
# Hard refresh browser (Ctrl + Shift + R)
# Or clear GitHub cache by adding ?v=2 to URL
```

---

## Quick Command Summary

```cmd
# 1. Remove model from Git (if needed)
git rm --cached best_siamese_model.pth

# 2. Add to .gitignore
echo *.pth >> .gitignore

# 3. Stage all changes
git add .

# 4. Commit
git commit -m "Optimize for Railway deployment"

# 5. Push
git push origin main
```

---

## What Gets Pushed to GitHub

### ✅ Included:
- All code files (`.py`, `.html`, `.css`)
- `requirements.txt` (without PyTorch)
- Documentation (`.md` files)
- Configuration files (`Procfile`, `railway.json`, etc.)
- `.gitignore`

### ❌ Excluded (in .gitignore):
- `best_siamese_model.pth` (too large)
- `*.pth`, `*.pt` (all model files)
- `.env` (secrets)
- `__pycache__/` (Python cache)
- `db.sqlite3` (local database)
- `media/verification_photos/` (user photos)

---

## After Pushing

### Railway will automatically:
1. Detect the push
2. Start building
3. Install dependencies from `requirements.txt`
4. Run migrations
5. Start the server

### Monitor deployment:
1. Go to Railway dashboard
2. Click your project
3. Watch "Deployments" tab
4. Check logs for any errors

---

## Verification Checklist

After pushing, verify:

- [ ] GitHub repo updated
- [ ] `best_siamese_model.pth` NOT in repo
- [ ] `requirements.txt` has no PyTorch
- [ ] New documentation files visible
- [ ] Railway starts building automatically
- [ ] No build errors in Railway logs
- [ ] App deploys successfully
- [ ] Can sign up and use app

---

## 🎃 You're Ready!

Once pushed, Railway will automatically deploy your optimized app!

**Deployment URL**: Check Railway dashboard for your app URL

**Test it**:
1. Visit your Railway URL
2. Click "Rise from the Grave"
3. Sign up with WorkOS
4. Should go to "Tell Kiro" page
5. Fill form and add GitHub link
6. Portfolio should generate

**Everything should work!** 🚀
