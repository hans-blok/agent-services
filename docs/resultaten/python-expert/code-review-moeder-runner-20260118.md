# Code Review — Moeder Runner (op_fetch_agents)

**Reviewer**: Python Expert  
**Datum**: 2026-01-18  
**Bestand**: `exports/utility/runners/moeder/core.py`  
**Functie**: `op_fetch_agents` (regels 325-602)  
**Focus**: Runner module folders worden niet correct geteld

---

## Samenvatting

De `op_fetch_agents` functie in de moeder runner kopieert agents uit agent-services naar een workspace. De code kopieert correct zowel standalone runner files (`moeder.py`) als runner module folders (`moeder/`), maar telt alleen de standalone files mee in de statistieken. Dit leidt tot incorrecte rapportage.

**Complexiteit**: Gemiddeld (±180 regels, file operations met Git en JSON)  
**Scope**: Agent provisioning vanuit remote repository  
**Python versie**: 3.10+ (type hints met `|` operator)

---

## Bevindingen

### Kritiek

**K1. Runner module folders worden niet geteld in statistieken**

**Locatie**: Regels 437-443 (runner module kopiëren)

**Probleem**:
```python
# Runner module folder (indien aanwezig)
runner_module_src = repo_path / "exports" / value_stream / "runners" / agent_naam
if runner_module_src.exists() and runner_module_src.is_dir():
    runner_module_dst = workspace_root / "scripts" / agent_naam
    if runner_module_dst.exists():
        shutil.rmtree(runner_module_dst)
    shutil.copytree(runner_module_src, runner_module_dst)
    artifacts.append(runner_module_dst)
```

De code kopieert de module folder correct, maar verhoogt `runners_count` niet. Hierdoor:
- Statistieken in manifest zijn incorrect
- Fetch-log toont verkeerde aantallen
- Gebruiker denkt dat module folders niet zijn geïnstalleerd

**Aanbeveling**:
```python
# Runner module folder (indien aanwezig)
runner_module_src = repo_path / "exports" / value_stream / "runners" / agent_naam
if runner_module_src.exists() and runner_module_src.is_dir():
    runner_module_dst = workspace_root / "scripts" / agent_naam
    if runner_module_dst.exists():
        shutil.rmtree(runner_module_dst)
    shutil.copytree(runner_module_src, runner_module_dst)
    artifacts.append(runner_module_dst)
    runners_count += 1  # ← TOEVOEGEN
```

**Impact**: **HOOG** - Gebruiker verwacht volledige runners maar krijgt verkeerde feedback.

---

### Belangrijk

**B1. Inconsistente telling: file vs module worden beide als "1 runner" geteld**

**Locatie**: Regels 428-443

**Probleem**:
Een agent kan zowel `moeder.py` (file) als `moeder/` (module folder) hebben. De huidige code telt beide als "1 runner", maar conceptueel is dit dezelfde runner (alleen met verschillende structuur).

**Aanbeveling**:
Twee opties:

**Optie A: Tel alles (conservatief)**
```python
# File
if runner_src.exists():
    # ... copy ...
    runners_count += 1

# Module (altijd tellen, ook als er ook een file is)
if runner_module_src.exists() and runner_module_src.is_dir():
    # ... copy ...
    runners_count += 1
```

**Optie B: Tel als één runner (logisch)**
```python
runner_found = False

# File
if runner_src.exists():
    # ... copy ...
    runner_found = True

# Module
if runner_module_src.exists() and runner_module_src.is_dir():
    # ... copy ...
    runner_found = True

if runner_found:
    runners_count += 1
```

Ik adviseer **Optie B** omdat agents-publicatie.json ook "1 runner" rapporteert per agent (ongeacht file/module structuur).

**Impact**: **GEMIDDELD** - Statistieken kloppen niet met werkelijke architectuur.

---

**B2. Geen validatie dat runner module dependencies aanwezig zijn**

**Locatie**: Regels 437-443

**Probleem**:
Als een runner module wordt gekopieerd (bijv. `moeder/`), wordt niet gevalideerd of:
- De module een `__init__.py` heeft
- De parent runner file (`moeder.py`) ook wordt gekopieerd
- De module importeerbaar is

Voor `moeder.py` die `from moeder.frontdoor import run_frontdoor` doet, moet zowel `moeder.py` als `moeder/` folder aanwezig zijn.

**Aanbeveling**:
```python
# Na kopiëren, valideer module integriteit
if runner_module_dst.exists():
    init_file = runner_module_dst / "__init__.py"
    if not init_file.exists():
        # Waarschuwing toevoegen aan artifacts/logs
        print(f"[WARNING] Runner module {agent_naam}/ heeft geen __init__.py")
```

**Impact**: **GEMIDDELD** - Geïnstalleerde runners kunnen non-functional zijn.

---

**B3. shutil.rmtree zonder error handling**

**Locatie**: Regel 441

**Probleem**:
```python
if runner_module_dst.exists():
    shutil.rmtree(runner_module_dst)
```

Kan falen bij:
- Permission errors (Windows file locks)
- Symlinks in de module folder
- Read-only files

**Aanbeveling**:
```python
if runner_module_dst.exists():
    try:
        shutil.rmtree(runner_module_dst)
    except (PermissionError, OSError) as e:
        raise PolicyError(
            f"Kan bestaande runner module niet verwijderen: {runner_module_dst}\n"
            f"Fout: {e}\n"
            f"Tip: Sluit programma's die deze files gebruiken en probeer opnieuw."
        )
```

**Impact**: **GEMIDDELD** - Kan installatie blokkeren zonder duidelijke foutmelding.

---

### Nice-to-have

**N1. Dubbele datetime.now() calls in log generatie**

**Locatie**: Regels 459-462

**Probleem**:
```python
log_lines = [
    f"# Fetch Agents Log\n\n",
    f"**Datum**: {datetime.now().strftime('%Y-%m-%d')}\n",
    f"**Tijd**: {datetime.now().strftime('%H:%M:%S')}\n",
```

Twee calls naar `datetime.now()` kunnen (theoretisch) verschillende tijden geven als de seconde overslaat tussen calls.

**Aanbeveling**:
```python
log_timestamp = datetime.now()
log_lines = [
    f"# Fetch Agents Log\n\n",
    f"**Datum**: {log_timestamp.strftime('%Y-%m-%d')}\n",
    f"**Tijd**: {log_timestamp.strftime('%H:%M:%S')}\n",
```

**Impact**: **LAAG** - Cosmetisch, zeer onwaarschijnlijk in praktijk.

---

**N2. Inconsistente artifact logging voor module folders**

**Locatie**: Regel 443

**Probleem**:
```python
artifacts.append(runner_module_dst)
```

Voor een folder append je het folder Path object, maar voor files append je ook het file Path. In de trace wordt dit consistent gerenderd via `relative_to()`, maar het zou helderder zijn om expliciet aan te geven dat het een folder is.

**Aanbeveling**:
Geen wijziging nodig, maar overweeg toekomstig om een dataclass te gebruiken:
```python
@dataclass
class ArtifactInfo:
    path: Path
    type: str  # 'file' | 'directory'
```

**Impact**: **LAAG** - Code werkt correct, alleen traceability verbetering.

---

## Positieve Punten

✓ **Correcte Git operaties**: Clone met `--depth 1` is efficient  
✓ **Goede error handling**: PolicyError bij missing manifest, invalid value-stream  
✓ **Cleanup via context manager**: Temp directory wordt automatisch opgeruimd  
✓ **Traceability**: Manifest en logs worden gegenereerd  
✓ **Type hints**: Consistent gebruik van moderne Python type annotations  
✓ **Idempotentie**: Overschrijven van bestaande modules is correct geïmplementeerd

---

## Top 3 Actiepunten

### 1. **FIX: Tel runner module folders mee in statistieken** (Kritiek)
- Locatie: Regel 443
- Actie: Voeg `runners_count += 1` toe na `shutil.copytree()`
- Prioriteit: **URGENT** - Gebruiker krijgt verkeerde feedback

### 2. **IMPROVE: Consistente runner telling (file + module = 1 runner)** (Belangrijk)
- Locatie: Regels 428-443
- Actie: Gebruik `runner_found` boolean om file én module als één runner te tellen
- Prioriteit: **HOOG** - Align met agents-publicatie.json semantiek

### 3. **HARDEN: Error handling voor shutil.rmtree** (Belangrijk)
- Locatie: Regel 441
- Actie: Wrap in try-except met PolicyError en nuttige user guidance
- Prioriteit: **GEMIDDELD** - Voorkom cryptische failures op Windows

---

## Code Snippet: Complete Fix

```python
# Runners (optioneel)
if include_runners:
    runner_found = False  # Track of deze agent een runner heeft
    
    # Standalone runner file
    runner_src = repo_path / "exports" / value_stream / "runners" / f"{agent_naam}.py"
    if runner_src.exists():
        runner_dst = workspace_root / "scripts" / f"{agent_naam}.py"
        runner_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(runner_src, runner_dst)
        artifacts.append(runner_dst)
        runner_found = True
    
    # Runner module folder (indien aanwezig)
    runner_module_src = repo_path / "exports" / value_stream / "runners" / agent_naam
    if runner_module_src.exists() and runner_module_src.is_dir():
        runner_module_dst = workspace_root / "scripts" / agent_naam
        
        # Verwijder bestaande module (met error handling)
        if runner_module_dst.exists():
            try:
                shutil.rmtree(runner_module_dst)
            except (PermissionError, OSError) as e:
                raise PolicyError(
                    f"Kan bestaande runner module niet verwijderen: {runner_module_dst}\n"
                    f"Fout: {e}\n"
                    f"Tip: Sluit programma's die deze files gebruiken."
                )
        
        # Kopieer module
        shutil.copytree(runner_module_src, runner_module_dst)
        artifacts.append(runner_module_dst)
        runner_found = True
        
        # Valideer module heeft __init__.py
        init_file = runner_module_dst / "__init__.py"
        if not init_file.exists():
            print(f"[WARNING] Runner module {agent_naam}/ heeft geen __init__.py", file=sys.stderr)
    
    # Tel als 1 runner (ongeacht file/module structuur)
    if runner_found:
        runners_count += 1

installed_count += 1
```

---

**Conclusie**: De code is grotendeels goed, maar heeft een kritiek bug in statistiek-telling die directe impact heeft op gebruikerservaring. De fix is eenvoudig (1 regel toevoegen), maar ik adviseer ook de conceptuele verbetering (file + module = 1 runner) door te voeren voor consistency met het agent register.
