@echo off
echo Cleaning Git history to remove secrets...
echo.

REM Remove the problematic files from Git history
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch WORKOS_MIGRATION.md WORKOS_TROUBLESHOOTING.md .env.example" --prune-empty --tag-name-filter cat -- --all

echo.
echo Adding back the cleaned files...
git add WORKOS_MIGRATION.md WORKOS_TROUBLESHOOTING.md .env.example

echo.
echo Committing cleaned files...
git commit -m "Remove secrets from documentation files"

echo.
echo Force pushing to GitHub...
git push origin main --force

echo.
echo Done! Your repository is now clean.
pause
