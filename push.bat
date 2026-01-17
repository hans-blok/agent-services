@echo off
REM Commit and Push Script
REM Usage: commit-push.bat "commit message"

IF "%~1"=="" (
    echo ERROR: Commit message is required
    echo Usage: commit-push.bat "commit message"
    exit /b 1
)

echo ========================================
echo Git Commit and Push
echo ========================================
echo.

echo Step 1: Adding files to staging...
git add -A
IF ERRORLEVEL 1 (
    echo ERROR: Failed to add files
    exit /b 1
)
echo ✓ Files staged

echo.
echo Step 2: Committing with message: %~1
git commit -m "%~1"
IF ERRORLEVEL 1 (
    echo ERROR: Failed to commit
    exit /b 1
)
echo ✓ Committed

echo.
echo Step 3: Pushing to remote...
git push
IF ERRORLEVEL 1 (
    echo ERROR: Failed to push
    exit /b 1
)
echo ✓ Pushed

echo.
echo ========================================
echo SUCCESS: All changes committed and pushed
echo ========================================
