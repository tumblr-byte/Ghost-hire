# 🚂 Railway Deployment Notes

## Changes for Railway Deployment

### ✅ What's Included:
- Django backend
- MySQL database
- WorkOS authentication
- GitHub portfolio analysis
- All community features (crews, jobs, etc.)
- SerpAPI reverse image search

### ❌ What's Excluded (Too Heavy):
- PyTorch (removed from requirements.txt)
- Siamese neural network model (~500MB)
- Photo verification with face detection

## Why These Changes?

**Railway Free/Hobby Tier Limitations:**
- Limited memory (~512MB-1GB)
- Limited storage
- PyTorch alone is ~800MB
- Siamese model is ~500MB
- **Total**: Would exceed 1.3GB just for ML

**Solution:**
- Skip photo verification on Railway
- Auto-verify users on signup
- Keep Siamese code in repo (for judges to see)
- Full ML features work locally for demo video

## User Flow Comparison

### Local (Full Features):
1. Sign up with WorkOS ✅
2. Upload verification photo ✅
3. Siamese network checks duplicate ✅
4. SerpAPI checks if photo exists online ✅
5. Tell Kiro about yourself ✅
6. Add GitHub link & analyze ✅
7. View haunted portfolio ✅

### Railway (Lightweight):
1. Sign up with WorkOS ✅
2. ~~Upload verification photo~~ (skipped)
3. ~~Siamese network checks~~ (skipped)
4. ~~SerpAPI checks~~ (skipped)
5. Tell Kiro about yourself ✅
6. Add GitHub link & analyze ✅
7. View haunted portfolio ✅

## What Judges See

### In GitHub Repo:
- ✅ Full Siamese network code
- ✅ ML implementation details
- ✅ README_SIAMESE.md explaining architecture
- ✅ Complete verification flow

### In Demo Video:
- ✅ Siamese network working locally
- ✅ Duplicate face detection
- ✅ Full verification flow
- ✅ All features demonstrated

### On Railway Deployment:
- ✅ Working app (lightweight)
- ✅ All core features
- ❌ Photo verification (explained in README)

## For Hackathon Judges

**Message to Judges:**

> "We built a Siamese Neural Network for face verification (see code in repo and demo video). For the live Railway deployment, we disabled photo verification to fit within free tier limits. The ML code demonstrates our understanding of deep learning - we didn't just use APIs, we built the model ourselves. In production, we'd use AWS Rekognition or deploy the model on a dedicated GPU server."

## Technical Details

### Removed from requirements.txt:
```
torch==2.7.1          # ~800MB
torchvision==0.22.1   # ~200MB
```

### Modified in auth_views.py:
```python
# Auto-verify users (skip photo verification)
if not user.is_verified:
    user.is_verified = True
    user.save()
```

### Kept in Codebase:
- `haunted_profiles/utils.py` - Siamese network code
- `best_siamese_model.pth` - Model file (gitignored, too large)
- `README_SIAMESE.md` - Full ML documentation

## Deployment Size Comparison

### With PyTorch (Local):
- Django: ~50MB
- PyTorch: ~800MB
- Siamese Model: ~500MB
- Other deps: ~100MB
- **Total: ~1.45GB** ❌ Too large for Railway

### Without PyTorch (Railway):
- Django: ~50MB
- Other deps: ~100MB
- **Total: ~150MB** ✅ Fits Railway free tier

## Future Production Deployment

For a production deployment with full ML features:

### Option 1: Cloud ML Service
- Use AWS Rekognition Face Comparison
- Cost: ~$0.001 per comparison
- No model hosting needed

### Option 2: Separate ML Service
- Deploy Siamese model on AWS EC2 with GPU
- Main app on Railway
- API calls between services

### Option 3: Upgrade Railway Plan
- Railway Pro plan: More memory/storage
- Can include PyTorch
- Cost: ~$20/month

## Testing the Deployment

### Before Deploying:
```bash
# Test without PyTorch locally
pip uninstall torch torchvision
python manage.py runserver
# Should work without photo verification
```

### After Deploying:
1. Sign up with WorkOS ✅
2. Should skip directly to "Tell Kiro" page ✅
3. Fill profile and GitHub link ✅
4. Portfolio should generate ✅
5. All other features work ✅

## Environment Variables for Railway

Make sure these are set:
```env
DEBUG=False
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=your-app.up.railway.app
WORKOS_CLIENT_ID=<your-client-id>
WORKOS_API_KEY=<your-api-key>
WORKOS_REDIRECT_URI=https://your-app.up.railway.app/auth/callback/
SERPAPI_KEY=<your-serpapi-key>
```

## 🎃 Summary

**For Judges:**
- Code shows we built ML (Siamese network)
- Demo video shows it working
- Railway deployment is lightweight but functional
- We understand production tradeoffs

**For Users:**
- Railway: Fast signup, no photo needed
- Local: Full verification with ML
- Both: Complete platform features

This approach demonstrates:
1. ✅ ML/AI skills (built Siamese network)
2. ✅ Production thinking (deployment optimization)
3. ✅ Full-stack capabilities (working app)
4. ✅ Pragmatic decisions (tradeoffs for constraints)

---

**Ready to deploy!** 🚀
