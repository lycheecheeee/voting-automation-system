@echo off
chcp 65001 >nul
echo ========================================
echo   Voting Automation - Vercel Deploy
echo ========================================
echo.

echo [Step 1] Checking Vercel CLI...
where vercel >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm i -g vercel
)
echo.

echo [Step 2] Deploying to Vercel...
vercel --prod --yes

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Set environment variables in Vercel dashboard
echo 2. Visit your Vercel URL
echo.
pause
