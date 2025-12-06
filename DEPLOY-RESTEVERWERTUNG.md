# Deployment: Resteverwertungs-Feature

## 📋 Auf dem Pi ausführen

### 1. Code pullen
```bash
cd ~/kitchenhelper-ai
git pull origin main
```

### 2. DB-Migration ausführen
```bash
# WICHTIG: Aus dem richtigen Verzeichnis!
cd ~/kitchenhelper-ai

# Migration ausführen
sqlite3 backend/data/kitchen.db < backend/migrate_add_quantity_unit.sql

# Verify (sollte quantity und unit zeigen!)
sqlite3 backend/data/kitchen.db "PRAGMA table_info(ingredients);"
```

### 3. Backend neustarten
```bash
cd ~/kitchenhelper-ai/backend
docker-compose down
docker-compose up -d --build

# Logs prüfen
docker-compose logs -f --tail=50
```

## ✅ Test-Szenario

1. **Zutat mit Menge hinzufügen:**
   - Name: Hackfleisch
   - Menge: 1000
   - Einheit: g
   - Kategorie: Fleisch

2. **Rezept generieren:**
   - Hackfleisch auswählen
   - Rezept generieren (sollte z.B. 500g verwenden)

3. **Als gekocht markieren:**
   - Button "✅ Als gekocht markieren" klicken
   - Bestätigen

4. **Menge prüfen:**
   - Zu Zutaten gehen
   - Hackfleisch sollte jetzt 500g zeigen (statt 1000g)!

## 🐛 Troubleshooting

**Fehler: "column quantity does not exist"**
→ Migration nicht ausgeführt oder falscher DB-Pfad

**Fehler: "reduce_ingredient_quantity not found"**
→ Backend nicht neu gestartet

**Mengen werden nicht reduziert:**
→ Logs prüfen: `docker-compose logs backend`
