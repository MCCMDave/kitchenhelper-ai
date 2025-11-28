# 🔐 Datenverschlüsselung - Konzept

## Übersicht

Dieses Dokument beschreibt die Verschlüsselungsstrategie für Benutzerdaten in KitchenHelper-AI, insbesondere für Pro-Nutzer.

## Schutzziele

### Was muss verschlüsselt werden?
1. **Persönliche Daten (DSGVO-relevant)**
   - E-Mail-Adressen
   - Benutzernamen (optional)
   - Passwörter (bereits als Hash gespeichert)

2. **Ernährungsdaten (sensibel)**
   - Ernährungsprofile (Allergien, Unverträglichkeiten)
   - Gesundheitsinformationen (Diabetiker, etc.)

3. **Nutzerdaten (weniger kritisch, aber Pro-Feature)**
   - Zutaten
   - Lieblingsrezepte
   - Generierte Rezepte

## Verschlüsselungsarchitektur

### Option 1: End-to-End Encryption (E2EE) ⭐ EMPFOHLEN

**Vorteile:**
- ✅ Höchste Sicherheit
- ✅ Server kann Daten nicht lesen (Zero-Knowledge)
- ✅ Starkes Verkaufsargument für Pro

**Nachteile:**
- ❌ Komplexere Implementierung
- ❌ Passwort-Verlust = Datenverlust
- ❌ Schwieriger zu debuggen

**Implementierung:**
```javascript
// Client-Side (Browser)
1. User-Passwort → Schlüsselableitung (PBKDF2/Argon2)
2. Master-Key generieren (AES-256-GCM)
3. Daten verschlüsseln BEVOR sie zum Server gesendet werden
4. Server speichert nur verschlüsselte Daten

// Beim Login:
1. User-Passwort → Schlüsselableitung
2. Verschlüsselte Daten vom Server laden
3. Im Browser entschlüsseln
```

**Technologie-Stack:**
- **Web Crypto API** (nativ im Browser, kein npm-Package nötig)
- **Argon2** für Key Derivation (sichere Passwort-zu-Key Ableitung)
- **AES-256-GCM** für Verschlüsselung

---

### Option 2: Server-Side Encryption (SSE)

**Vorteile:**
- ✅ Einfachere Implementierung
- ✅ Passwort-Reset möglich
- ✅ Admin kann bei Problemen helfen

**Nachteile:**
- ❌ Server kann Daten lesen
- ❌ Schwächere Sicherheit bei Server-Kompromittierung
- ❌ Weniger Marketing-Power

**Implementierung:**
```python
# Server-Side (Backend)
1. Master-Key im Environment (.env)
2. Daten mit AES-256 verschlüsseln vor DB-Speicherung
3. Entschlüsseln wenn User Daten abruft
```

**Technologie-Stack:**
- **Python `cryptography`** Library
- **Fernet** (symmetrische Verschlüsselung)
- Master-Key in `.env`

---

## 💎 Empfohlene Lösung: Hybrid-Ansatz

**Best of both worlds:**

### Für Pro-Nutzer (E2EE):
- End-to-End Encryption für sensible Daten
- Ernährungsprofile verschlüsselt
- Rezepte verschlüsselt (optional)

### Für Free-Nutzer (SSE):
- Server-Side Encryption
- Einfacher, aber immer noch sicher
- Upgrade-Anreiz zu Pro

### Implementierung:

```javascript
// frontend/js/crypto.js
const Crypto = {
    // Generate encryption key from password
    async deriveKey(password, salt) {
        const enc = new TextEncoder();
        const keyMaterial = await window.crypto.subtle.importKey(
            "raw",
            enc.encode(password),
            "PBKDF2",
            false,
            ["deriveBits", "deriveKey"]
        );

        return window.crypto.subtle.deriveKey(
            {
                name: "PBKDF2",
                salt: salt,
                iterations: 100000,
                hash: "SHA-256"
            },
            keyMaterial,
            { name: "AES-GCM", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );
    },

    // Encrypt data
    async encrypt(data, key) {
        const enc = new TextEncoder();
        const iv = window.crypto.getRandomValues(new Uint8Array(12));

        const encrypted = await window.crypto.subtle.encrypt(
            { name: "AES-GCM", iv: iv },
            key,
            enc.encode(JSON.stringify(data))
        );

        return {
            iv: Array.from(iv),
            data: Array.from(new Uint8Array(encrypted))
        };
    },

    // Decrypt data
    async decrypt(encryptedData, key) {
        const decrypted = await window.crypto.subtle.decrypt(
            { name: "AES-GCM", iv: new Uint8Array(encryptedData.iv) },
            key,
            new Uint8Array(encryptedData.data)
        );

        const dec = new TextDecoder();
        return JSON.parse(dec.decode(decrypted));
    }
};
```

```python
# backend/app/crypto.py
from cryptography.fernet import Fernet
import os

class DataEncryption:
    def __init__(self):
        # Load master key from environment
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypt data (for Free tier users)"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

## Migration Plan

### Phase 1: Backend-Vorbereitung
1. ✅ Datenbank-Schema erweitern
   - `profiles` Tabelle: `encrypted_data` (TEXT/JSON)
   - `encryption_type` (ENUM: 'none', 'server', 'client')
2. ✅ Server-Side Encryption implementieren
3. ✅ Migration-Script für bestehende Daten

### Phase 2: Client-Side Encryption
1. ✅ `crypto.js` Modul erstellen
2. ✅ Pro-User bei Login: Encryption-Key ableiten
3. ✅ Profile/Rezepte verschlüsseln vor Upload

### Phase 3: Testing
1. ✅ Unit Tests für Verschlüsselung
2. ✅ Integration Tests
3. ✅ Security Audit

### Phase 4: Rollout
1. ✅ Free-User: Server-Side (transparent)
2. ✅ Pro-User: Optional E2EE aktivieren
3. ✅ Später: E2EE verpflichtend für Pro

## Datenbank-Schema

```sql
-- Erweitere profiles Tabelle
ALTER TABLE profiles ADD COLUMN encrypted_data TEXT;
ALTER TABLE profiles ADD COLUMN encryption_type VARCHAR(20) DEFAULT 'none';
ALTER TABLE profiles ADD COLUMN encryption_salt BLOB;

-- Für verschlüsselte Rezepte (optional)
ALTER TABLE recipes ADD COLUMN encrypted BOOLEAN DEFAULT FALSE;
ALTER TABLE recipes ADD COLUMN encrypted_content TEXT;
```

## Security Best Practices

### ✅ DOs:
- Master-Key NIEMALS im Code
- Master-Key in `.env` oder Secrets Manager
- HTTPS/TLS für alle Übertragungen
- Regelmäßige Security Audits
- Key-Rotation-Strategie

### ❌ DON'Ts:
- Keys im Git-Repository
- ECB-Mode verwenden (unsicher!)
- Eigene Crypto implementieren
- IV/Nonce wiederverwenden

## Performance-Überlegungen

**Verschlüsselung ist schnell:**
- AES-GCM: ~1ms für 1KB Daten
- PBKDF2 (100k iterations): ~50ms (einmalig beim Login)
- Negligible Performance-Impact

**Caching:**
- Encryption-Key im Memory während Session
- Entschlüsselte Daten im LocalStorage (optional, Risiko!)

## DSGVO-Compliance

✅ **Vorteile für Compliance:**
- Daten "pseudonymisiert" wenn verschlüsselt
- Weniger Risiko bei Data Breach
- Stärkt "Privacy by Design"

⚠️ **Beachten:**
- User muss über Verschlüsselung informiert werden
- Passwort-Verlust = Datenverlust muss klar sein
- Backup-/Recovery-Strategie dokumentieren

## Kosten

**Entwicklungszeit:**
- Option 1 (E2EE): ~20-30 Stunden
- Option 2 (SSE): ~8-12 Stunden
- Hybrid: ~25-35 Stunden

**Laufende Kosten:**
- Keine zusätzlichen Infrastruktur-Kosten
- CPU-Overhead: <5%

## Zusammenfassung

**Empfehlung:** Hybrid-Ansatz
- **Free:** Server-Side Encryption (einfach, sicher genug)
- **Pro:** Client-Side E2EE (Marketing + maximale Sicherheit)

**Nächste Schritte:**
1. Backend-Schema erweitern
2. `crypto.js` implementieren
3. Server-Side Encryption als Basis
4. E2EE für Pro als Premium-Feature

---

**Status:** 📋 Konzept-Phase
**Verantwortlich:** Dave Vaupel
**Erstellt:** 2025-01-28
**Review:** TBD
