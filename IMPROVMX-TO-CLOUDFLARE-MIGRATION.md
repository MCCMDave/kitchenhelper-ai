# Migration: ImprovMX → Cloudflare Email Routing

**Domain:** kitchenhelper-ai.de
**Datum:** 05.12.2025
**Ziel:** E-Mail-Empfang von ImprovMX zu Cloudflare Email Routing migrieren

---

## 📋 Übersicht

**Aktuelle Situation:**
- **VERSAND:** Resend.com (Subdomain `send.kitchenhelper-ai.de`) ✅
- **EMPFANG:** ImprovMX (Root-Domain `@`) ⚠️ Soll zu Cloudflare migriert werden

**Problem:**
- ImprovMX und Cloudflare Email Routing konkurrieren um die gleichen MX Records auf `@`
- Cloudflare Email Routing wurde aktiviert, aber ImprovMX MX Records sind noch vorhanden
- Ergebnis: E-Mail-Empfang funktioniert nicht richtig

**Lösung:**
- ImprovMX MX Records entfernen
- Cloudflare Email Routing MX Records hinzufügen
- SPF Record anpassen (ImprovMX entfernen, Cloudflare hinzufügen)

---

## ⚠️ WICHTIG: Backup vor Migration

**Vor der Migration:**
1. ✅ Screenshot aller DNS-Records machen (Cloudflare Dashboard)
2. ✅ ImprovMX Weiterleitung dokumentieren (welche Adressen wohin)
3. ✅ Test-E-Mail an `info@kitchenhelper-ai.de` senden und prüfen ob sie ankommt

---

## 🔧 Schritt 1: Cloudflare Email Routing aktivieren

### 1.1 Dashboard öffnen

1. Login auf [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Domain **kitchenhelper-ai.de** auswählen
3. Linke Sidebar: **Email** → **Email Routing**

### 1.2 Email Routing aktivieren

1. Klicke auf **"Get started"** oder **"Enable Email Routing"**
2. Cloudflare zeigt dir die DNS-Records, die automatisch hinzugefügt werden:
   - **MX Records:** `amir.mx.cloudflare.net`, `isaac.mx.cloudflare.net`, `linda.mx.cloudflare.net`
   - **TXT Record (SPF):** `v=spf1 include:_spf.mx.cloudflare.net ~all`

3. **WICHTIG:** Klicke **NOCH NICHT** auf "Add records and enable"!
   - Grund: ImprovMX MX Records müssen erst entfernt werden

---

## 🔧 Schritt 2: ImprovMX DNS-Records entfernen

### 2.1 Zu DNS-Records navigieren

1. Cloudflare Dashboard → **kitchenhelper-ai.de**
2. Linke Sidebar: **DNS** → **Records**

### 2.2 ImprovMX MX Records löschen

**Folgende Records LÖSCHEN:**

| Typ | Name | Priorität | Ziel |
|-----|------|-----------|------|
| MX  | @    | 10        | mx1.improvmx.com |
| MX  | @    | 20        | mx2.improvmx.com |

**So löschen:**
1. Suche nach den MX Records mit "mx1.improvmx.com" und "mx2.improvmx.com"
2. Klicke auf **"Edit"** (Stift-Symbol)
3. Klicke auf **"Delete"** (Mülleimer-Symbol)
4. Bestätige die Löschung

### 2.3 SPF Record anpassen

**Aktueller SPF Record:**
```
@ TXT v=spf1 include:spf.improvmx.com include:amazonses.com ~all
```

**Neuer SPF Record (ImprovMX entfernen, Cloudflare hinzufügen):**
```
@ TXT v=spf1 include:_spf.mx.cloudflare.net include:amazonses.com ~all
```

**So ändern:**
1. Suche nach dem TXT Record mit `v=spf1 include:spf.improvmx.com`
2. Klicke auf **"Edit"**
3. Ersetze `spf.improvmx.com` mit `_spf.mx.cloudflare.net`
4. Klicke auf **"Save"**

---

## 🔧 Schritt 3: Cloudflare Email Routing aktivieren

### 3.1 MX Records automatisch hinzufügen

1. Zurück zu **Email** → **Email Routing**
2. Klicke auf **"Add records and enable"**
3. Cloudflare fügt automatisch die MX Records hinzu:
   - `@ MX 69 amir.mx.cloudflare.net`
   - `@ MX 48 isaac.mx.cloudflare.net`
   - `@ MX 70 linda.mx.cloudflare.net`

4. Status sollte auf **"Active"** wechseln

### 3.2 Destination Address verifizieren

1. Cloudflare sendet eine Bestätigungs-E-Mail an `studio.del.melucio@gmail.com`
2. Öffne die E-Mail und klicke auf den Verifizierungs-Link
3. Status in Cloudflare sollte auf **"Verified"** wechseln

---

## 🔧 Schritt 4: Routing Rules konfigurieren

### 4.1 Custom Addresses einrichten

1. **Email** → **Email Routing** → **Routing rules**
2. Klicke auf **"Create address"**

**Adressen einrichten:**

| Custom Address | Action | Destination |
|----------------|--------|-------------|
| `info@kitchenhelper-ai.de` | Send to an email | `studio.del.melucio@gmail.com` |
| `contact@kitchenhelper-ai.de` | Send to an email | `studio.del.melucio@gmail.com` |
| `kontakt@kitchenhelper-ai.de` | Send to an email | `studio.del.melucio@gmail.com` |
| `support@kitchenhelper-ai.de` | Send to an email | `studio.del.melucio@gmail.com` |

**Für jede Adresse:**
1. **Custom address:** z.B. `info@kitchenhelper-ai.de`
2. **Action:** "Send to an email"
3. **Destination address:** `studio.del.melucio@gmail.com`
4. Klicke auf **"Save"**

### 4.2 Catch-All einrichten

1. Scroll nach unten zu **"Catch-all address"**
2. Toggle auf **"Enabled"**
3. **Action:** "Send to an email"
4. **Destination:** `studio.del.melucio@gmail.com`
5. Klicke auf **"Save"**

**Was macht Catch-All?**
- Fängt alle E-Mails an Adressen ohne spezifische Regel ab
- Beispiel: `test@kitchenhelper-ai.de` → weitergeleitet an `studio.del.melucio@gmail.com`
- Nützlich für Tippfehler und unbekannte Adressen

---

## ✅ Schritt 5: Testen

### 5.1 DNS-Propagierung warten

- **Zeit:** 5-15 Minuten (manchmal bis zu 48 Stunden)
- **Prüfen:** `nslookup -type=MX kitchenhelper-ai.de`

**Erwartete Ausgabe:**
```
kitchenhelper-ai.de     mail exchanger = 69 amir.mx.cloudflare.net.
kitchenhelper-ai.de     mail exchanger = 48 isaac.mx.cloudflare.net.
kitchenhelper-ai.de     mail exchanger = 70 linda.mx.cloudflare.net.
```

### 5.2 Test-E-Mail senden

1. Sende eine E-Mail an `info@kitchenhelper-ai.de` von einem externen Account
2. Prüfe ob sie in `studio.del.melucio@gmail.com` ankommt
3. Prüfe den **Header** der E-Mail:
   - Sollte `Received: from ... mx.cloudflare.net` enthalten

### 5.3 Catch-All testen

1. Sende eine E-Mail an eine nicht existierende Adresse: `test12345@kitchenhelper-ai.de`
2. Sollte trotzdem in `studio.del.melucio@gmail.com` ankommen

---

## 📊 Endkonfiguration (Übersicht)

### DNS Records nach Migration

| Typ | Name | Wert | Zweck |
|-----|------|------|-------|
| MX | @ | 69 amir.mx.cloudflare.net | Cloudflare Email Routing |
| MX | @ | 48 isaac.mx.cloudflare.net | Cloudflare Email Routing |
| MX | @ | 70 linda.mx.cloudflare.net | Cloudflare Email Routing |
| TXT | @ | v=spf1 include:_spf.mx.cloudflare.net include:amazonses.com ~all | SPF (Cloudflare + Resend) |
| TXT | resend._domainkey | p=MIGfMA0GCSq... | DKIM (Resend) |
| TXT | _dmarc | v=DMARC1; p=none; | DMARC |
| MX | send | 10 feedback-smtp.eu-west-1.amazonses.com | Resend (Versand) |
| TXT | send | v=spf1 include:amazonses.com ~all | SPF (Resend Subdomain) |

### E-Mail-Funktionalität

| Funktion | Service | Status |
|----------|---------|--------|
| **E-Mail-VERSAND** | Resend.com (`noreply@kitchenhelper-ai.de`) | ✅ Bleibt unverändert |
| **E-Mail-EMPFANG** | Cloudflare Email Routing | ✅ Neu aktiviert |
| **Weiterleitung** | `*@kitchenhelper-ai.de` → `studio.del.melucio@gmail.com` | ✅ Catch-All |

---

## 🚨 Troubleshooting

### Problem: E-Mails kommen nicht an

**Ursache 1: DNS nicht propagiert**
- **Lösung:** Warte 15-30 Minuten, teste erneut
- **Prüfen:** `nslookup -type=MX kitchenhelper-ai.de`

**Ursache 2: Destination Address nicht verifiziert**
- **Lösung:** Prüfe Gmail-Posteingang für Verifizierungs-E-Mail
- **Check:** Cloudflare Dashboard → Status sollte "Verified" sein

**Ursache 3: ImprovMX Records noch vorhanden**
- **Lösung:** DNS Records erneut prüfen, ImprovMX MX Records löschen

### Problem: E-Mails landen im Spam

**Ursache:** SPF/DKIM/DMARC nicht korrekt
- **Lösung 1:** SPF Record prüfen (sollte `_spf.mx.cloudflare.net` enthalten)
- **Lösung 2:** DMARC Record hinzufügen falls nicht vorhanden
- **Lösung 3:** Warte 24-48h (Sender-Reputation baut sich auf)

### Problem: Catch-All funktioniert nicht

**Ursache 1:** Catch-All nicht aktiviert
- **Lösung:** Email Routing → Routing rules → Catch-all → Toggle auf "Enabled"

**Ursache 2:** Destination Address nicht verifiziert
- **Lösung:** Gmail-Posteingang prüfen, Verifizierungs-Link klicken

---

## 🔄 Rollback zu ImprovMX (falls nötig)

Falls Cloudflare Email Routing Probleme macht:

1. **Cloudflare Email Routing deaktivieren:**
   - Email → Email Routing → "Disable Email Routing"
   - MX Records werden automatisch entfernt

2. **ImprovMX MX Records wiederherstellen:**
   - DNS → Records → Add Record
   - `@ MX 10 mx1.improvmx.com`
   - `@ MX 20 mx2.improvmx.com`

3. **SPF Record anpassen:**
   - `v=spf1 include:spf.improvmx.com include:amazonses.com ~all`

4. **Warten:** 15-30 Minuten DNS-Propagierung

---

## 📝 Notizen

- **Resend.com** bleibt unverändert (Subdomain `send.kitchenhelper-ai.de`)
- **Keine Downtime** wenn DNS richtig konfiguriert
- **Free Plan:** Cloudflare Email Routing ist 100% kostenlos (unbegrenzte Weiterleitungen)
- **Logs:** Email Routing → Activity zeigt alle empfangenen E-Mails

---

## ✅ Checkliste

- [ ] Backup: Screenshot aller DNS-Records
- [ ] Backup: ImprovMX Weiterleitung dokumentiert
- [ ] ImprovMX MX Records gelöscht (mx1/mx2.improvmx.com)
- [ ] SPF Record angepasst (spf.improvmx.com → _spf.mx.cloudflare.net)
- [ ] Cloudflare Email Routing aktiviert ("Add records and enable")
- [ ] Destination Address verifiziert (studio.del.melucio@gmail.com)
- [ ] Custom Addresses konfiguriert (info@, contact@, kontakt@, support@)
- [ ] Catch-All aktiviert
- [ ] Test-E-Mail gesendet und empfangen
- [ ] Catch-All getestet (test12345@kitchenhelper-ai.de)
- [ ] Memory.md aktualisiert (ImprovMX → Cloudflare)

---

**Migration abgeschlossen?** → Aktualisiere `.claude/memory.md`:
- Entferne Zeilen 52-57 (ImprovMX DNS-Records)
- Behalte Zeilen 36-38 (Cloudflare Email Routing)
- Aktualisiere Zeile 59 auf: "Empfang-Adresse: info@kitchenhelper-ai.de (weitergeleitet via Cloudflare Email Routing)"
