@echo off
echo ========================================
echo Pushing Updates to GitHub
echo ========================================
echo.

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Removing model file from Git (if exists)...
git rm --cached best_siamese_model.pth 2>nul
if %errorlevel% equ 0 (
    echo [OK] Model file removed from Git
) else (
    echo [OK] Model file not in Git (already excluded)
)
echo.

echo Step 3: Adding all changes...
git add .
echo [OK] Changes staged
echo.

echo Step 4: Committing changes...
git commit -m "Optimize for Railway deployment - remove PyTorch, skip verification"
if %errorlevel% equ 0 (
    echo [OK] Changes committed
) else (
    echo [INFO] No changes to commit or already committed
)
echo.

echo Step 5: Pushing to GitHub...
git push origin main
if %errorlevel% equ 0 (
    echo [OK] Successfully pushed to GitHub!
) else (
    echo [ERROR] Push failed. Try force push? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        echo Force pushing...
        git push origin main --force
        echo [OK] Force pushed to GitHub!
    )
)
echo.

echo ========================================
echo Done! Check GitHub repo:
echo https://github.com/tumblr-byte/Ghost-hire
echo ========================================
echo.
echo Next: Railway will auto-deploy from GitHub
echo Monitor at: https://railway.app
echo.
pause
