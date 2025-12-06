# Kitchen Helper-AI - Rezept-Datenbank Konzept

## 🎯 Ziel
Eine lokale Rezept-Datenbank, die mit Ollama zusammenarbeitet und die Rezeptgenerierung verbessert.

---

## 📊 Datenbankgröße & Umfang

### Option 1: Kompakte Starter-DB (Empfohlen)
**Größe:** ~50-100 MB
**Anzahl Rezepte:** 1.000-2.000
**Inhalt:**
- Deutsche Grundrezepte (500)
- Internationale Klassiker (300)
- Vegetarische/Vegane Rezepte (200)
- Schnelle Gerichte (<30min) (200)
- Desserts & Backwaren (150)

**Vorteile:**
- ✅ Schnelle Ladezeiten
- ✅ Geringer Speicherverbrauch
- ✅ Einfache Wartung
- ✅ Funktioniert gut mit Ollama (llama3.2:3b)

---

### Option 2: Erweiterte DB
**Größe:** ~500 MB - 1 GB
**Anzahl Rezepte:** 10.000-20.000
**Inhalt:**
- Komplette Länderküchen (20+ Länder)
- Saisonale Rezepte
- Diät-spezifische Varianten
- Professionelle Koch-Techniken

**Vorteile:**
- ✅ Mehr Vielfalt
- ✅ Bessere Rezeptvorschläge
- ❌ Langsamere Suche ohne Index
- ❌ Benötigt mehr RAM

---

## 🏗️ Technische Architektur

### Datenbank-Format
```json
{
  "recipes": [
    {
      "id": "uuid-1234",
      "title": "Spaghetti Carbonara",
      "category": "italian",
      "difficulty": "easy",
      "cookTime": 20,
      "servings": 4,
      "ingredients": [
        {"name": "Spaghetti", "amount": 400, "unit": "g"},
        {"name": "Eier", "amount": 4, "unit": "stück"},
        {"name": "Parmesan", "amount": 100, "unit": "g"},
        {"name": "Pancetta", "amount": 150, "unit": "g"}
      ],
      "instructions": [
        "Spaghetti in Salzwasser kochen...",
        "Pancetta in Pfanne knusprig braten...",
        "Eier mit Parmesan verquirlen..."
      ],
      "tags": ["pasta", "schnell", "italienisch"],
      "nutrition": {
        "calories": 650,
        "protein": 28,
        "carbs": 75,
        "fat": 22
      },
      "allergens": ["gluten", "eier", "milch"]
    }
  ]
}
```

---

## 🔗 Integration mit Ollama

### Konzept 1: RAG (Retrieval-Augmented Generation)
**So funktioniert's:**
1. User fragt: "Was kann ich mit Tomaten, Mozzarella und Basilikum machen?"
2. Backend durchsucht Rezept-DB nach passenden Rezepten
3. Top 3 Rezepte werden an Ollama gegeben als Kontext
4. Ollama generiert personalisierte Antwort basierend auf echten Rezepten

**Beispiel-Prompt:**
```python
context = """
Gefundene Rezepte:
1. Caprese Salat (5min, einfach)
2. Tomate-Mozzarella Auflauf (30min, mittel)
3. Basilikum-Pesto mit Tomate (15min, einfach)
"""

prompt = f"""
Basierend auf diesen Rezepten:
{context}

Der Nutzer hat: Tomaten, Mozzarella, Basilikum
Erstelle ein detailliertes Rezept mit:
- Zutatenliste
- Schritt-für-Schritt Anleitung
- Kochzeit
- Schwierigkeitsgrad
"""
```

**Vorteil:**
- ✅ Ollama basiert auf echten, erprobten Rezepten
- ✅ Keine Halluzinationen (unrealistische Rezepte)
- ✅ Schnellere Generation (kleinerer Context)

---

### Konzept 2: Hybrid-Ansatz (Empfohlen!)
**Kombination aus DB + KI:**

**Schritt 1:** Suche in DB
```python
# Finde exakte Matches
exact_matches = db.search_by_ingredients(user_ingredients)

if len(exact_matches) > 0:
    # Zeige direkt Rezepte aus DB
    return exact_matches[0:3]
```

**Schritt 2:** KI-Generation mit DB-Kontext
```python
else:
    # Finde ähnliche Rezepte
    similar_recipes = db.search_similar(user_ingredients, limit=5)

    # Nutze ähnliche Rezepte als Inspiration für Ollama
    ollama_response = generate_recipe_with_context(
        ingredients=user_ingredients,
        inspiration=similar_recipes
    )
    return ollama_response
```

**Vorteil:**
- ✅ Schnell bei bekannten Kombinationen (direkt aus DB)
- ✅ Kreativ bei ungewöhnlichen Kombinationen (KI)
- ✅ Beste User Experience

---

## 📁 Datei-Struktur

```
backend/
├── data/
│   ├── recipes.db              # SQLite Datenbank (alternativ)
│   ├── recipes.json            # JSON Format (einfacher)
│   └── embeddings/             # Vektor-Embeddings für Suche
│       └── recipe-vectors.npy
├── services/
│   ├── recipe_search.py        # Rezept-Suche Engine
│   ├── recipe_rag.py           # RAG Integration
│   └── embedding_service.py    # Vektor-Suche
└── routes/
    └── recipes.py              # API Endpoints
```

---

## 🚀 Implementation Roadmap

### Phase 1: Basis-Datenbank (1-2 Tage)
- [ ] 500 Grund-Rezepte sammeln (deutsche Küche)
- [ ] JSON-Schema definieren
- [ ] SQLite Datenbank erstellen
- [ ] Einfache Suche implementieren (nach Zutaten)

### Phase 2: Ollama Integration (2-3 Tage)
- [ ] RAG-System implementieren
- [ ] Context-Builder für Ollama
- [ ] Hybrid-Ansatz (DB + KI)
- [ ] Caching für häufige Anfragen

### Phase 3: Erweiterte Features (optional)
- [ ] Vektor-Suche mit Embeddings
- [ ] Nutzer-Favoriten in DB speichern
- [ ] Rezept-Bewertungen
- [ ] Saisonale Empfehlungen

---

## 💾 Speicheranforderungen

### Kompakt-DB (1000 Rezepte):
- JSON: ~50 MB
- SQLite: ~30 MB (komprimiert)
- Embeddings: ~20 MB
- **Gesamt:** ~100 MB

### Erweitert-DB (10.000 Rezepte):
- JSON: ~500 MB
- SQLite: ~300 MB
- Embeddings: ~200 MB
- **Gesamt:** ~1 GB

---

## 🎯 Empfehlung für dich

**Start mit Kompakt-DB (500-1000 Rezepte):**
1. Schnell implementierbar
2. Funktioniert perfekt mit Ollama llama3.2:3b
3. Geringer RAM-Verbrauch (~100 MB zusätzlich)
4. Kann später erweitert werden

**Hybrid-Ansatz:**
- Exakte Matches aus DB (schnell)
- KI-Generation für neue Kombinationen (kreativ)
- Beste Balance zwischen Geschwindigkeit und Flexibilität

---

## 🔧 Technische Details

### Datenbank-Wahl
**Option A: SQLite** (Empfohlen)
```python
# Vorteile:
- Eingebaut in Python
- Schnelle Suche mit Indizes
- Transaktionen
- Keine zusätzliche Software
```

**Option B: JSON + In-Memory**
```python
# Vorteile:
- Einfacher zu editieren
- Schnell bei kleiner DB (<1000 Rezepte)
- Menschenlesbar
```

### Suche-Algorithmus
```python
def search_recipes(user_ingredients, db):
    # 1. Exakte Übereinstimmung
    exact = db.find_recipes_with_all(user_ingredients)
    if exact:
        return exact

    # 2. Partial Match (mindestens 70% Zutaten)
    partial = db.find_recipes_with_most(user_ingredients, threshold=0.7)
    if partial:
        return partial

    # 3. Kategorie-basiert
    categories = infer_categories(user_ingredients)
    similar = db.find_by_category(categories)

    # 4. Ollama mit Kontext
    return ollama_generate_with_context(user_ingredients, similar)
```

---

## 📈 Performance-Schätzung

**Ollama llama3.2:3b (auf deinem PC):**
- Ohne DB-Kontext: 10-15 Sekunden
- Mit DB-Kontext (RAG): 8-12 Sekunden (schneller!)
- Direkt aus DB: <1 Sekunde

**Vorteil DB + Ollama:**
- 20-30% schnellere Generierung
- Konsistentere Rezepte
- Weniger "Halluzinationen"

---

## 🎁 Bonus: Datenquellen

**Kostenlose Rezept-Datenbanken:**
1. **RecipeDB** (Open Source): 10.000+ Rezepte
2. **Food.com Dataset**: 180.000 Rezepte (Kaggle)
3. **Allrecipes Scraper**: Custom crawler
4. **Deutsche Rezepte**: Chefkoch.de API (falls verfügbar)

**Lizenz-Hinweis:** Bei scraping immer Nutzungsbedingungen prüfen!

---

## 💡 Fazit

**Empfohlener Ansatz:**
1. Start mit 1.000 Rezepten in SQLite
2. Hybrid-System (DB + Ollama)
3. RAG für bessere KI-Antworten
4. Später auf 10.000+ erweitern

**Größe:** ~100 MB initial, ~1 GB maximal
**Kompatibel mit Ollama:** ✅ Ja, perfekt!
**Implementierungsaufwand:** 2-5 Tage
**Performance-Gewinn:** 20-30% schneller + bessere Qualität

---

**Bereit für Implementation?** Lass mich wissen, ob du mit Phase 1 starten möchtest! 🚀
