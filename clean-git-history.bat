@echo off
echo ========================================
echo Cleaning Git History - Removing Secrets
echo ========================================
echo.

echo Step 1: Backing up current branch...
git branch backup-main

echo.
echo Step 2: Creating a fresh orphan branch...
git checkout --orphan temp-main

echo.
echo Step 3: Adding all current files (with cleaned secrets)...
git add -A

echo.
echo Step 4: Creating fresh commit...
git commit -m "Initial commit - clean version without secrets"

echo.
echo Step 5: Deleting old main branch...
git branch -D main

echo.
echo Step 6: Renaming temp branch to main...
git branch -m main

echo.
echo Step 7: Force pushing to GitHub...
git push -f origin main

echo.
echo ========================================
echo Done! Git history is now clean.
echo ========================================
echo.
echo If something went wrong, restore with:
echo git checkout backup-main
echo.
pause
