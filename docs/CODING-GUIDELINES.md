# 📝 CODING GUIDELINES & BEST PRACTICES

**Version:** 1.0  
**Erstellt:** 23. Oktober 2025  
**Zweck:** Syntaxfehler vermeiden, konsistente Scripts erstellen

---

## 🎯 ÜBERSICHT

Diese Richtlinien helfen dabei, fehlerfreie und wartbare Scripts zu erstellen.

**Wichtigste Regel:** KISS - Keep It Simple, Stupid! 🚀

---

## ⚡ POWERSHELL GUIDELINES

### 1. KRITISCH: Sonderzeichen vermeiden ❌

**Problem:** Bestimmte Zeichen verursachen Parsing-Fehler

**Verbotene Zeichen in Strings:**
```powershell
# ❌ FALSCH - Verursacht Fehler:
Write-Host "→ Pfeil"           # Unicode-Pfeil
Write-Host "═══════════"       # Box-Drawing Zeichen
Write-Host "CPU $i: Test"      # Doppelpunkt nach Variable in Here-String

# ✅ RICHTIG - ASCII-Zeichen verwenden:
Write-Host "> Pfeil"           # Normaler Pfeil
Write-Host "============"      # Normale Gleichheitszeichen
Write-Host "CPU Nr. $i Test"   # "Nr." statt Doppelpunkt
```

---

### 2. Here-Strings vermeiden (@"..."@)

**Problem:** Variablen mit `:` werden falsch interpretiert

**❌ FALSCH:**
```powershell
$Output += @"
CPU $i:
  Name: $name
"@
```

**✅ RICHTIG:**
```powershell
$Output += "CPU Nr. $i`n"
$Output += "  Name: $name`n"
```

**Oder wenn Here-String nötig:**
```powershell
# Variablen vorher auswerten
$cpuNumber = "CPU Nr. $i"
$Output += @"
$cpuNumber
  Name: $name
"@
```

---

### 3. Explizite Newlines verwenden

**❌ FALSCH:**
```powershell
$Output += "Zeile 1
Zeile 2"  # Impliziter Zeilenumbruch - kann Probleme machen
```

**✅ RICHTIG:**
```powershell
$Output += "Zeile 1`n"
$Output += "Zeile 2`n"
```

---

### 4. Variablennamen klar benennen

**❌ SCHLECHT:**
```powershell
$i = 1
$x = "test"
$tmp = Get-Process
```

**✅ GUT:**
```powershell
$counter = 1
$userName = "test"
$processList = Get-Process
```

---

### 5. Try-Catch immer verwenden

**❌ FALSCH:**
```powershell
$cpu = Get-CimInstance Win32_Processor
Write-Host $cpu.Name  # Kann fehlschlagen
```

**✅ RICHTIG:**
```powershell
try {
    $cpu = Get-CimInstance Win32_Processor
    Write-Host $cpu.Name
} catch {
    Write-Host "FEHLER: $($_.Exception.Message)" -ForegroundColor Red
}
```

---

### 6. Admin-Rechte prüfen

**Immer am Anfang des Scripts:**
```powershell
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "WARNUNG: Administrator-Rechte erforderlich!" -ForegroundColor Yellow
    exit 1
}
```

---

### 7. Encoding explizit setzen

**Bei Datei-Operationen:**
```powershell
# ✅ UTF-8 mit BOM
$content | Out-File -FilePath $path -Encoding UTF8

# ✅ UTF-8 ohne BOM (bevorzugt)
[System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
```

---

### 8. Parameter-Validierung

**Für robuste Scripts:**
```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$ComputerName,
    
    [Parameter(Mandatory=$false)]
    [ValidateRange(1, 100)]
    [int]$MaxResults = 10
)
```

---

### 9. Fortschrittsanzeige für lange Operationen

**Für bessere UX:**
```powershell
$items = 1..100
$total = $items.Count
$counter = 0

foreach ($item in $items) {
    $counter++
    $percentComplete = ($counter / $total) * 100
    Write-Progress -Activity "Verarbeite Items" -Status "$counter von $total" -PercentComplete $percentComplete
    
    # Deine Logik hier
    Start-Sleep -Milliseconds 50
}

Write-Progress -Activity "Verarbeite Items" -Completed
```

---

### 10. Keine hartcodierten Pfade

**❌ FALSCH:**
```powershell
$file = "C:\Users\david\Desktop\test.txt"
```

**✅ RICHTIG:**
```powershell
$file = Join-Path $env:USERPROFILE "Desktop\test.txt"
# oder
$file = "$env:USERPROFILE\Desktop\test.txt"
```

---

## 🐧 BASH GUIDELINES (Raspberry Pi)

### 1. Shebang immer setzen

```bash
#!/bin/bash
# oder für mehr Portabilität:
#!/usr/bin/env bash
```

---

### 2. Set Safety Options

```bash
#!/bin/bash

# Beende bei Fehler
set -e

# Beende bei undefinierter Variable
set -u

# Pipeline-Fehler weitergeben
set -o pipefail
```

---

### 3. Variablen in Quotes

**❌ FALSCH:**
```bash
file=$HOME/test.txt
rm $file  # Kann bei Leerzeichen fehlschlagen
```

**✅ RICHTIG:**
```bash
file="$HOME/test.txt"
rm "$file"
```

---

### 4. Funktionen verwenden

```bash
#!/bin/bash

# Funktion definieren
backup_database() {
    local db_name=$1
    local backup_dir=$2
    
    echo "Backup von $db_name nach $backup_dir..."
    # Backup-Logik hier
}

# Funktion aufrufen
backup_database "nextcloud" "/home/dave/backups"
```

---

### 5. Exit-Codes verwenden

```bash
#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "FEHLER: Docker nicht installiert!"
    exit 1
fi

# Script erfolgreich
exit 0
```

---

### 6. Logging implementieren

```bash
#!/bin/bash

LOG_FILE="/var/log/mein-script.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Script gestartet"
log "Führe Backup aus..."
```

---

### 7. Berechtigungen prüfen

```bash
#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
    echo "Dieses Script muss als root ausgeführt werden!"
    exit 1
fi
```

---

## 🧪 TESTING-CHECKLISTE

### Vor dem Ausrollen eines Scripts:

- [ ] **Syntax-Check:**
  - PowerShell: `Get-Command .\script.ps1` 
  - Bash: `bash -n script.sh`

- [ ] **Test mit verschiedenen Inputs:**
  - Normale Werte
  - Leere Werte
  - Ungültige Werte
  - Extremwerte

- [ ] **Fehlerbehandlung:**
  - Try-Catch vorhanden?
  - Exit-Codes korrekt?
  - Fehler-Meldungen hilfreich?

- [ ] **Pfade & Berechtigungen:**
  - Keine hartcodierten Pfade?
  - Admin-Rechte geprüft?
  - Dateien existieren?

- [ ] **Sonderzeichen-Check:**
  - Keine Unicode-Zeichen (→, ═, etc.)?
  - Keine Tilden in kritischen Stellen?
  - ASCII-only in kritischen Bereichen?

- [ ] **Dokumentation:**
  - Kommentare vorhanden?
  - Zweck erklärt?
  - Parameter dokumentiert?

---

## 📊 SCRIPT-TEMPLATE POWERSHELL

```powershell
<#
.SYNOPSIS
    Kurze Beschreibung des Scripts

.DESCRIPTION
    Detaillierte Beschreibung was das Script macht

.PARAMETER ComputerName
    Name des Computers

.EXAMPLE
    .\script.ps1 -ComputerName "PC01"
    
.NOTES
    Version: 1.0
    Autor: Dave
    Datum: 2025-10-23
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ComputerName
)

# Admin-Rechte prüfen
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "FEHLER: Administrator-Rechte erforderlich!" -ForegroundColor Red
    exit 1
}

# Hauptlogik
try {
    Write-Host "Starte Script..." -ForegroundColor Cyan
    
    # Deine Logik hier
    
    Write-Host "Script erfolgreich abgeschlossen!" -ForegroundColor Green
    exit 0
    
} catch {
    Write-Host "FEHLER: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
```

---

## 📊 SCRIPT-TEMPLATE BASH

```bash
#!/bin/bash

#############################################
# Script Name: mein-script.sh
# Beschreibung: Was macht das Script?
# Autor: Dave
# Datum: 2025-10-23
# Version: 1.0
#############################################

# Safety options
set -euo pipefail

# Variablen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/var/log/mein-script.log"

# Funktionen
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    log "FEHLER: $1"
    exit 1
}

# Root-Check
if [ "$EUID" -ne 0 ]; then 
    error_exit "Dieses Script muss als root ausgeführt werden!"
fi

# Hauptlogik
log "Script gestartet"

# Deine Logik hier

log "Script erfolgreich abgeschlossen"
exit 0
```

---

## 🎯 WICHTIGSTE REGELN (ZUSAMMENFASSUNG)

### PowerShell:
1. ✅ **Keine Sonderzeichen** (→, ═, ~) in kritischen Bereichen
2. ✅ **Here-Strings vermeiden** oder ohne `:` nach Variablen
3. ✅ **Explizite Newlines** (``n`) verwenden
4. ✅ **Try-Catch überall** wo es fehlschlagen kann
5. ✅ **Admin-Rechte prüfen** wenn nötig

### Bash:
1. ✅ **Safety options** (`set -euo pipefail`)
2. ✅ **Variablen in Quotes** (`"$variable"`)
3. ✅ **Exit-Codes verwenden** (0 = Erfolg, 1+ = Fehler)
4. ✅ **Logging implementieren**
5. ✅ **Funktionen für Wiederverwendbarkeit**

### Beide:
1. ✅ **Klare Variablennamen**
2. ✅ **Kommentare schreiben**
3. ✅ **Keine hartcodierten Pfade**
4. ✅ **Fehlerbehandlung immer**
5. ✅ **Testen vor Deployment**

---

## 📚 WEITERFÜHRENDE RESSOURCEN

### PowerShell:
- [PowerShell Best Practices](https://docs.microsoft.com/en-us/powershell/scripting/learn/ps101/01-getting-started)
- [PowerShell Style Guide](https://poshcode.gitbook.io/powershell-practice-and-style/)

### Bash:
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://www.shellcheck.net/) - Online Syntax Checker

---

## 🔄 CHANGELOG

### v1.0 (23. Oktober 2025)
- Initiale Version erstellt
- PowerShell Guidelines
- Bash Guidelines
- Testing-Checkliste
- Script-Templates

---

**Letzte Aktualisierung:** 23. Oktober 2025  
**Bei Fragen oder Ergänzungen:** Einfach Claude fragen!
