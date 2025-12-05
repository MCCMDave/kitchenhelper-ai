# 🚀 Deploy to Raspberry Pi

## WICHTIG: Backend muss aktualisiert werden!

Das Backend auf dem Pi läuft noch mit alter CORS-Konfiguration, die Inkognito-Login verhindert.

### Deployment Steps:

```bash
# 1. SSH zum Pi
ssh pi  # oder: ssh pi-t (Tailscale)

# 2. Navigate to Backend
cd ~/kitchenhelper-api  # Oder wo auch immer dein Backend liegt

# 3. Pull latest changes
git pull origin main

# 4. Restart Docker Container
docker restart kitchenhelper-api
# ODER wenn du docker-compose nutzt:
docker-compose restart

# 5. Verify
docker logs kitchenhelper-api --tail 50
```

### Was wird gefixt:

- ✅ CORS Wildcard (`*`) → Spezifische Origins
- ✅ `allow_credentials=True` für httpOnly Cookies
- ✅ Inkognito-Modus Login funktioniert

### Erwartetes Ergebnis:

Nach Deploy sollte Login im Inkognito-Modus ohne "Server not reachable" funktionieren!

---

**Erstellt:** 05.12.2025 17:50
