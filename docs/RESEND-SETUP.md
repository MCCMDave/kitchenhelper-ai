# Resend.com E-Mail Setup für KitchenHelper-AI

## Übersicht

KitchenHelper-AI nutzt **Resend.com** für den E-Mail-Versand:
- **User-Registrierung:** E-Mail-Verifizierung
- **Passwort-Reset:** Sicherer Reset-Link
- **Rate Limiting:** Automatische Begrenzung (100 E-Mails/Tag im Free Plan)
- **Retry-Logik:** Automatische Wiederholung bei temporären Fehlern

---

## 📋 Voraussetzungen

- [ ] Domain registriert (z.B. bei Porkbun oder Namecheap)
- [ ] Resend.com Account erstellt
- [ ] Python 3.8+ installiert

---

## 🚀 Setup-Schritte

### 1. Resend.com Account erstellen

1. Gehe zu [resend.com](https://resend.com)
2. Registriere dich kostenlos
3. Bestätige deine E-Mail-Adresse

**Free Plan Limits:**
- 100 E-Mails/Tag
- 3.000 E-Mails/Monat
- 1 Domain
- 2 Requests/Sekunde

---

### 2. API-Key generieren

1. Navigiere zu **API Keys** im Dashboard
2. Klicke auf **"Create API Key"**
3. Wähle **"Sending Access"** (empfohlen für Produktion)
4. Kopiere den Key sofort (wird nur einmal angezeigt!)

**Format:** `re_xxxxxxxxx`

---

### 3. Domain zu Resend hinzufügen

#### 3.1 Domain hinzufügen

1. Gehe zu **Domains** im Resend Dashboard
2. Klicke auf **"Add Domain"**
3. Trage deine Domain ein

**Empfehlung:** Verwende eine Subdomain (z.B. `mail.deinedomain.de`)

**Vorteile:**
- Isolierte Sender-Reputation
- Klare Kommunikationsintention
- Einfachere Troubleshooting

#### 3.2 DNS-Records konfigurieren

Resend benötigt **zwei obligatorische DNS-Records**:

**1. SPF Record (TXT)**
- **Typ:** TXT Record
- **Name:** `@` (oder deine Subdomain)
- **Wert:** Wird von Resend bereitgestellt (ähnlich wie `v=spf1 include:resend.com ~all`)

**2. DKIM Record (TXT/CNAME)**
- **Typ:** CNAME oder TXT Record
- **Name:** Wird von Resend bereitgestellt (z.B. `resend._domainkey`)
- **Wert:** Wird von Resend bereitgestellt

**3. DMARC Record (Optional, empfohlen)**
- **Typ:** TXT Record
- **Name:** `_dmarc`
- **Wert:** `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`

#### 3.3 DNS-Records beim Domain-Provider hinzufügen

**Beispiel für Porkbun/Namecheap:**

1. Logge dich bei deinem Domain-Provider ein
2. Navigiere zu **DNS Management**
3. Füge die von Resend bereitgestellten Records hinzu
4. Speichern

**Wichtig:** DNS-Propagierung kann 12-24 Stunden dauern!

#### 3.4 Verifizierung prüfen

**Tools zum Testen:**
- [dns.email](https://dns.email) - Resend's DNS-Lookup-Tool
- [MXToolbox](https://mxtoolbox.com) - Externe Verifizierung
- [DMARC Analyzer](https://www.dmarcanalyzer.com)

**Status-Optionen:**
- `pending` - Resend prüft aktiv die DNS-Records
- `verified` ✅ - Domain erfolgreich verifiziert
- `failed` - DNS-Records nicht innerhalb 72 Stunden erkannt

---

### 4. Backend konfigurieren

#### 4.1 Umgebungsvariablen setzen

Erstelle eine `.env` Datei im `backend/` Verzeichnis:

```bash
# Kopiere .env.example zu .env
cp .env.example .env
```

**Füge deine Resend-Credentials hinzu:**

```env
# Email Service (Resend.com)
RESEND_API_KEY=re_xxxxxxxxx  # Dein API Key

# From Email (WICHTIG: Nach Domain-Verifizierung ändern!)
RESEND_FROM_EMAIL=KitchenHelper <noreply@yourdomain.com>

# Reply-To Email (optional)
RESEND_REPLY_TO=support@yourdomain.com
```

**Wichtig:**
- Ersetze `yourdomain.com` mit deiner verifizierten Domain
- API-Key **NIEMALS** in Git committen!
- `.env` ist bereits in `.gitignore`

#### 4.2 Dependencies installieren

```bash
cd backend
pip install resend python-dotenv
```

Oder mit requirements.txt:

```bash
pip install -r requirements.txt
```

---

## 📧 Verfügbare API-Endpoints

### 1. E-Mail-Verifizierung senden

**POST** `/api/email/send-verification`

**Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Verifizierungs-E-Mail wurde gesendet",
  "email_id": "re_abc123..."
}
```

---

### 2. E-Mail verifizieren (Token)

**POST** `/api/email/verify`

**Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "E-Mail erfolgreich verifiziert!",
  "email": "user@example.com"
}
```

---

### 3. Passwort-Reset anfordern

**POST** `/api/email/request-password-reset`

**Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Falls ein Account mit dieser E-Mail existiert, wurde ein Reset-Link gesendet",
  "email_id": "re_xyz789..."
}
```

**Hinweis:** Gibt immer `success: true` zurück (Security Best Practice)

---

### 4. Passwort zurücksetzen

**POST** `/api/email/reset-password`

**Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "new_password": "new_secure_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Passwort erfolgreich zurückgesetzt",
  "email": "user@example.com"
}
```

---

### 5. Verifizierungs-E-Mail erneut senden

**GET** `/api/email/resend-verification`

**Requires:** Authentication (Bearer Token)

**Response:**
```json
{
  "success": true,
  "message": "Verifizierungs-E-Mail wurde erneut gesendet",
  "email_id": "re_def456..."
}
```

---

### 6. E-Mail-Status prüfen

**GET** `/api/email/status`

**Requires:** Authentication (Bearer Token)

**Response:**
```json
{
  "email": "user@example.com",
  "verified": true,
  "verified_at": "2025-12-01T10:30:00Z"
}
```

---

## 🧪 Testing

### Lokales Testing (Laptop)

Während die Domain-Verifizierung läuft, nutze die Resend Test-Domain:

```env
RESEND_FROM_EMAIL=KitchenHelper <onboarding@resend.dev>
```

**Wichtig:** Nur für Entwicklung! In Produktion immer eigene Domain verwenden.

### Test-Script

```python
# test_email.py
import os
from dotenv import load_dotenv
from app.services.email_service import EmailService

load_dotenv()

email_service = EmailService()

# Test Verification Email
result = email_service.send_verification_email(
    to="your-email@example.com",
    verification_url="http://localhost:8000/verify?token=test123",
    user_name="TestUser"
)

print(result)
```

```bash
python test_email.py
```

---

## 📊 Monitoring

### Rate Limiting

Der EmailService hat eingebautes Rate Limiting:

- **100 E-Mails/Tag** (Free Plan)
- **2 Requests/Sekunde**

Bei Überschreitung:
```python
Exception: "Daily email limit reached (100/day)"
```

### Logging

Alle E-Mails werden automatisch geloggt:

```
[INFO] Sending email to user@example.com - Subject: Verifiziere deine E-Mail-Adresse
[INFO] Email sent successfully - ID: re_abc123...
```

**Log-Level anpassen:**

```python
import logging
logging.getLogger("app.services.email_service").setLevel(logging.DEBUG)
```

---

## ⚠️ Troubleshooting

### Problem: "RESEND_API_KEY not found"

**Lösung:**

1. Prüfe, ob `.env` Datei existiert
2. Prüfe, ob `RESEND_API_KEY` gesetzt ist
3. Starte Backend neu

```bash
cat .env | grep RESEND_API_KEY
```

---

### Problem: "Domain not verified"

**Lösung:**

1. Prüfe DNS-Records mit [dns.email](https://dns.email)
2. Warte bis zu 24 Stunden auf DNS-Propagierung
3. Für Tests: Nutze `onboarding@resend.dev`

---

### Problem: "Rate limit exceeded (429)"

**Lösung:**

- Free Plan Limit erreicht (100/Tag)
- Warte bis nächster Tag (UTC Midnight)
- Upgrade zu Pro Plan ($20/Monat, 50.000/Monat)

---

### Problem: E-Mails landen im Spam

**Ursachen:**

1. SPF/DKIM/DMARC nicht korrekt konfiguriert
2. Fehlende Plain-Text-Alternative
3. Spam-Trigger-Wörter ("Free", "Winner", "Click here now")
4. Niedrige Sender-Reputation (neue Domain)

**Lösungen:**

- Alle DNS-Records verifizieren
- Subdomain verwenden (bessere Reputation)
- Professionelle, klare Sprache verwenden
- Unsubscribe-Link hinzufügen
- Domain "warm-up" (langsam steigern)

**Test-Tools:**
- [mail-tester.com](https://www.mail-tester.com) - Spam-Score checken (Ziel: 10/10)

---

## 🔒 Sicherheit

### API-Key Best Practices

✅ **DO:**
- API-Keys in `.env` speichern
- `.env` zu `.gitignore` hinzufügen
- Verschiedene Keys für Dev/Test/Prod
- Keys regelmäßig rotieren (alle 90 Tage)
- `sending_access` Keys verwenden (nicht `full_access`)

❌ **DON'T:**
- API-Keys nie im Code hardcoden
- Nie in Git committen
- Nicht in öffentlichen Repositories teilen

### Token-Sicherheit

- Verification-Tokens laufen nach **24 Stunden** ab
- Reset-Tokens laufen nach **24 Stunden** ab
- Tokens sind JWT-basiert (HMAC-SHA256)

---

## 📚 Weitere Ressourcen

**Offizielle Dokumentation:**
- [Resend API Reference](https://resend.com/docs)
- [Python SDK](https://resend.com/docs/send-with-python)
- [FastAPI Guide](https://resend.com/docs/send-with-fastapi)
- [Domain Setup](https://resend.com/docs/dashboard/domains/introduction)

**Tools:**
- [dns.email](https://dns.email) - DNS-Check
- [MXToolbox](https://mxtoolbox.com) - Email-Testing
- [mail-tester.com](https://www.mail-tester.com) - Spam-Score

---

## 🎯 Next Steps

1. [ ] Domain registrieren (Porkbun/Namecheap)
2. [ ] Resend Account erstellen
3. [ ] Domain zu Resend hinzufügen
4. [ ] DNS-Records konfigurieren
5. [ ] 24h warten (DNS-Propagierung)
6. [ ] `.env` konfigurieren mit API-Key
7. [ ] Backend neu starten
8. [ ] Test-E-Mail senden
9. [ ] Spam-Score prüfen (mail-tester.com)
10. [ ] Produktiv schalten! 🚀

---

## 💡 Tipps

- **Subdomain verwenden:** Bessere Reputation und Isolation
- **DMARC aktivieren:** Erhöht Vertrauen bei Mailbox-Providern
- **Warm-up:** Starte mit wenigen E-Mails/Tag, steigere langsam
- **Monitoring:** Nutze Resend Dashboard für Delivery-Stats
- **Bounce-Handling:** Entferne ungültige E-Mail-Adressen automatisch

---

**Status:** ✅ Integration abgeschlossen - Bereit für Domain-Verifizierung!

**Fragen?** Siehe [Resend Docs](https://resend.com/docs) oder KitchenHelper Issue Tracker.
