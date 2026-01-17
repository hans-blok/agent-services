@echo off
REM Batch file wrapper voor pull-repo.ps1

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Pull Repository Script
echo ========================================
echo.

REM Controleer of repository naam is opgegeven
if "%1"=="" (
    echo [FOUT] Repository naam is vereist
    echo.
    echo Gebruik: pull [repository-naam]
    echo Voorbeeld: pull mijn-repo
    echo.
    pause
    exit /b 1
)

echo [INFO] Repository: %1
echo [INFO] Script locatie: %~dp0
echo.

REM Controleer of het PowerShell script bestaat
if not exist "%~dp0pull-repo.ps1" (
    echo [FOUT] Pull-repo.ps1 niet gevonden op: %~dp0pull-repo.ps1
    echo.
    pause
    exit /b 1
)

echo [INFO] PowerShell script gevonden, wordt uitgevoerd...
echo.

REM Voer het PowerShell script uit met verbeterde error handling
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%~dp0pull-repo.ps1' -RepoName %1" 2>&1

set /a RESULT=%errorlevel%

if !RESULT! neq 0 (
    echo.
    echo [FOUT] Script is mislukt met exit code: !RESULT!
    echo.
    pause
    exit /b !RESULT!
)

echo.
echo [SUCCES] Pull voltooid!
echo.
pause
endlocal
