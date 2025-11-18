@echo off
echo ========================================
echo Security Check - Scanning for Secrets
echo ========================================
echo.

echo Checking for WorkOS API keys...
findstr /S /I /C:"sk_test_a2V5" *.* 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Found WorkOS API key!
) else (
    echo [OK] No WorkOS API keys found
)

echo.
echo Checking for WorkOS Client IDs...
findstr /S /I /C:"client_01K9KSPA3JEWWA2R99437QVPEQ" *.* 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Found WorkOS Client ID!
) else (
    echo [OK] No WorkOS Client IDs found
)

echo.
echo Checking for SerpAPI keys...
findstr /S /I /C:"86d19a769b3630651a2810ece7ec6234ffeb00ac" *.* 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Found SerpAPI key!
) else (
    echo [OK] No SerpAPI keys found
)

echo.
echo Checking for MySQL passwords...
findstr /S /I /C:"XOxyFTYEYNSRlNoOvecnQzZYGJRiTxxp" *.* 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Found MySQL password!
) else (
    echo [OK] No MySQL passwords found
)

echo.
echo Checking for Railway host...
findstr /S /I /C:"yamanote.proxy.rlwy.net" *.* 2>nul
if %errorlevel% equ 0 (
    echo [WARNING] Found Railway host!
) else (
    echo [OK] No Railway hosts found
)

echo.
echo ========================================
echo Security Check Complete
echo ========================================
echo.
echo Files that SHOULD contain secrets (ignored by Git):
echo - .env (your actual secrets - NOT committed)
echo.
echo Files that are SAFE to commit:
echo - .env.example (placeholder values only)
echo - All .md files (now cleaned)
echo.
pause
