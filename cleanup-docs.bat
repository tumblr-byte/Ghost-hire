@echo off
echo ========================================
echo Cleaning Up Unnecessary Documentation
echo ========================================
echo.

echo Keeping IMPORTANT files:
echo - README.md (main project description)
echo - README_SIAMESE.md (ML implementation)
echo - DEPLOYMENT_NOTES.md (production decisions)
echo.

echo Deleting OPTIONAL files:
del DEPLOYMENT.md 2>nul
del DEPLOY_CHECKLIST.md 2>nul
del UPDATE_GITHUB_GUIDE.md 2>nul
del RAILWAY_DEPLOYMENT.md 2>nul
del WORKOS_MIGRATION.md 2>nul
del WORKOS_TROUBLESHOOTING.md 2>nul
del FIX_REDIRECT_URI.md 2>nul
del QUICKSTART.md 2>nul
del AI_ANALYSIS_FEATURES.md 2>nul
del AI_ANALYSIS_IMPROVED.md 2>nul
del COMMUNITY_FEATURES_PLAN.md 2>nul
del COMPLETION_SUMMARY.md 2>nul
del FINAL_SETUP.md 2>nul
del FINAL_SUMMARY.md 2>nul
del FIX_REFRESH_BUTTON.md 2>nul
del GEN_Z_PORTFOLIO_FEATURE.md 2>nul
del GHOST_CREW_FEATURE.md 2>nul
del HOW_TO_ANALYZE_GITHUB.md 2>nul
del PORTFOLIO_DISPLAY_COMPLETE.md 2>nul
del PROJECT_COMPLETE.md 2>nul
del PROJECT_SUMMARY.md 2>nul
del SELF_DESCRIPTION_FEATURE.md 2>nul
del TEMPLATES_TODO.md 2>nul
del WHAT_DISPLAYS.md 2>nul
del WORKOS_AUTHENTICATION_SETUP.md 2>nul
del WORKOS_DASHBOARD_GUIDE.md 2>nul

echo.
echo [OK] Cleanup complete!
echo.
echo Remaining documentation:
echo - README.md
echo - README_SIAMESE.md
echo - DEPLOYMENT_NOTES.md
echo.
echo ========================================
echo Ready for GitHub!
echo ========================================
pause
