@echo off
REM Batch file wrapper voor fetch_agents.py
REM Haalt agents op uit remote repo en ordent ze lokaal per value-stream

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Fetch Agents Script
echo ========================================
echo.

REM Controleer of value-stream naam is opgegeven
if "%1"=="" (
    echo [FOUT] Value-stream naam is vereist
    echo.
    echo Gebruik: fetch-agents ^<value-stream^> [--source-repo ^<url^>] [--no-cleanup]
    echo.
    echo Voorbeelden:
    echo   fetch-agents kennispublicatie
    echo   fetch-agents it-development
    echo   fetch-agents utility --no-cleanup
    echo.
    pause
    exit /b 1
)

echo [INFO] Value-stream: %1
if not "%2"=="" echo [INFO] Extra argumenten: %2 %3 %4
echo [INFO] Script locatie: %~dp0
echo.

REM Controleer of Python script bestaat
if not exist "%~dp0scripts\fetch_agents.py" (
    echo [FOUT] fetch_agents.py niet gevonden op: %~dp0scripts\fetch_agents.py
    echo.
    pause
    exit /b 1
)

echo [INFO] Python script gevonden, wordt uitgevoerd...
echo.

REM Voer het Python script uit met alle argumenten doorgegeven
python "%~dp0scripts\fetch_agents.py" %* 2>&1

set /a RESULT=%errorlevel%

echo.

if !RESULT! neq 0 (
    echo [FOUT] Script is mislukt met exit code: !RESULT!
    echo.
    pause
    exit /b !RESULT!
) else (
    echo [SUCCES] Agents succesvol opgehaald en georganiseerd
    echo.
    pause
)

exit /b !RESULT!
