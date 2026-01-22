@echo off
REM ==============================================================================
REM Publiceer Agents Overzicht
REM ==============================================================================
REM
REM Doel:
REM   Voert agent-curator runner uit voor volledige agents publicatie.
REM   Genereert agents-publicatie.json en markdown archief met digest.
REM
REM Output:
REM   - agents-publicatie.json (root, voor fetch_agents.py)
REM   - docs/resultaten/agent-publicaties/agents-publicatie-YYYYMMDD-HHMMSS.md
REM
REM Gebruik:
REM   publiceer-agents.bat
REM
REM Traceability:
REM   - Runner: scripts/runners/agent-curator.py
REM   - Charter: agent-charters/charter.agent-curator.md
REM
REM ==============================================================================

echo.
echo ========================================
echo  Agent Curator - Publiceer Overzicht
echo ========================================
echo.

REM Controleer of Python beschikbaar is
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python niet gevonden. Installeer Python 3.9+ en probeer opnieuw.
    pause
    exit /b 1
)

REM Controleer of runner script bestaat
if not exist "scripts\runners\agent-curator.py" (
    echo [ERROR] Runner niet gevonden: scripts\runners\agent-curator.py
    pause
    exit /b 1
)

REM Voer agent-curator uit met volledige scope
echo [INFO] Start volledige agents publicatie...
echo.

python scripts\runners\agent-curator.py --scope volledig

REM Controleer exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Publicatie mislukt. Zie bovenstaande foutmeldingen.
    echo.
    pause
    exit /b 1
)

REM Succes
echo.
echo [SUCCESS] Publicatie voltooid!
echo.
echo Output bestanden:
echo   - agents-publicatie.json
echo   - docs\resultaten\agent-publicaties\agents-publicatie-[timestamp].md
echo.

pause
exit /b 0
