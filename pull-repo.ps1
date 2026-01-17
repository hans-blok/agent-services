param(
    [Parameter(Mandatory=$true, HelpMessage="Repository naam op GitHub")]
    [string]$RepoName
)

$ErrorActionPreference = "Stop"

try {
    # GitHub basis URL
    $GitHubUser = "hans-blok"
    $GitHubUrl = "https://github.com/$GitHubUser/$RepoName.git"
    $CurrentLocation = Get-Location
    
    Write-Host "[INFO] Huidige locatie: $CurrentLocation" -ForegroundColor Cyan
    Write-Host "[INFO] Repository naam: $RepoName" -ForegroundColor Cyan
    Write-Host "[INFO] GitHub URL: $GitHubUrl" -ForegroundColor Cyan
    Write-Host ""
    
    # Controleer of Git geïnstalleerd is
    try {
        $gitVersion = git --version
        Write-Host "[OK] Git gevonden: $gitVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "[FOUT] Git is niet geïnstalleerd of niet in PATH" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    
    # Controleer of de repository al lokaal bestaat
    if (Test-Path $RepoName) {
        Write-Host "[INFO] Repository '$RepoName' gevonden, wordt geupdatet..." -ForegroundColor Yellow
        
        Push-Location $RepoName
        
        try {
            $output = git pull 2>&1
            Write-Host $output
            
            Write-Host "[OK] Pull succesvol voltooid!" -ForegroundColor Green
        }
        catch {
            Write-Host "[FOUT] Fout bij git pull: $_" -ForegroundColor Red
            exit 1
        }
        finally {
            Pop-Location
        }
    }
    else {
        Write-Host "[INFO] Repository '$RepoName' niet gevonden, wordt gecloned..." -ForegroundColor Yellow
        
        try {
            # Voer git clone direct uit zonder output capture zodat interactieve auth werkt
            & git clone $GitHubUrl
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[OK] Clone succesvol voltooid!" -ForegroundColor Green
            }
            else {
                Write-Host "[FOUT] Git clone mislukt met exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
        }
        catch {
            Write-Host "[FOUT] Fout bij git clone: $_" -ForegroundColor Red
            Write-Host "[FOUT] Controleer of de repository bestaat: $GitHubUrl" -ForegroundColor Red
            exit 1
        }
    }
}
catch {
    Write-Host "[FOUT] Onverwachte fout: $_" -ForegroundColor Red
    Write-Host "[FOUT] Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    exit 1
}
