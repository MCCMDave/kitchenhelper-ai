# KitchenHelper-AI - Monetarisierung mit Diabetiker-Fokus

## 🎯 Mission: Diabetiker unterstützen, NICHT reich werden

**Kernphilosophie:**
- App soll funktionieren und hilfreich sein für ALLE Diabetiker
- Monetarisierung = Kostendeckung + nachhaltige Entwicklung
- Soziale Mission > Business-Optimierung
- **Kritische Diabetiker-Features müssen kostenlos sein**

---

## 💰 Freemium + 3 Premium Tiers (Diabetiker-optimiert)

### **FREE TIER** 🆓 - Vollständig funktional für Diabetiker
**Zielgruppe:** ALLE Diabetiker, Einsteiger, Studenten, Menschen mit wenig Budget

**Philosophie:** Jeder Diabetiker soll die App nutzen können, ohne zu zahlen.

**Features:**
✅ **Unbegrenzte Rezept-Generierung** (langsam, 76s Durchschnitt)
✅ **Basis-Nährwerte:** Kalorien, Kohlenhydrate, Protein, Fett, Ballaststoffe ⭐
✅ **Broteinheiten (BE) Berechnung** (Kohlenhydrate ÷ 12) ⭐
✅ **10 Favoriten speichern**
✅ **PDF-Export für Favoriten** (max 10 PDFs) ⭐
✅ **3 Sprachen** (DE, EN, FR)
✅ **Basis-Präferenzen:** Vegetarisch, Low-Carb, Glutenfrei
✅ **Diabetiker-Filter (Basic):** Rezepte <30g Kohlenhydrate

❌ Keine Rezept-Datenbank (nur KI-Generierung via Ollama)
❌ Kein Glykämischer Index (GI/GL)
❌ Kein Meal-Planning
❌ Keine Wochenplanung mit Kohlenhydrat-Budget

**Warum das funktioniert:**
- Diabetiker können **Kohlenhydrate tracken** (kritisch!)
- BE-Berechnung ist automatisch (wichtig für Insulin-Berechnung)
- PDFs für wichtige Rezepte zum Ausdrucken (10 Stamm-Rezepte reichen)
- Performance ist langsam (76s), aber **kostenlos und vollständig funktional**
- Keine Paywall für lebensnotwendige Features

**Geschätzte Kosten pro User:** 0€ (self-hosted Ollama)

---

### **BASIC TIER** 🌱 - 2,99€/Monat
**Zielgruppe:** Aktive Diabetiker, die schnellere Rezepte wollen

**Philosophie:** Erschwinglich wie eine Tasse Kaffee, aber mit massiven Vorteilen.

**Features:**
✅ **Alles aus FREE Tier**
✅ **Kompakte Rezept-DB:** 1.000 kuratierte Rezepte
✅ **6x schnellere Generierung** (76s → 12s) ⚡
✅ **Glykämischer Index (GI)** ⭐
✅ **Glykämische Last (GL)** ⭐
✅ **Unbegrenzte Favoriten**
✅ **Unbegrenzte PDF-Exporte**
✅ **10 Sprachen** (statt 3)
✅ **Erweiterte Nährwerte:** Zucker, gesättigte Fettsäuren, Cholesterin
✅ **Einkaufslisten-Generator**
✅ **Diabetiker-Filter (Erweitert):** Low-Carb (<20g), Low-GI (<55), Diabetiker-freundlich

**Rezept-DB Inhalt (1.000 Rezepte):**
- 250 Low-Carb Rezepte (<20g KH)
- 200 Low-GI Rezepte (GI <55)
- 150 diabetiker-freundliche Desserts (Zuckerersatz)
- 200 schnelle Gerichte (<30min)
- 150 vegetarisch/vegan
- 50 glutenfrei

**Performance:**
- Bekannte Gerichte: Instant aus DB (<1s)
- Neue Kombinationen: 10-14s (KI mit DB-Kontext)
- **Durchschnitt: 12s** (6x schneller als FREE)

**Warum 2,99€?**
- Erschwinglich für ALLE (1x Kaffee pro Monat)
- GI/GL sind wichtig für Blutzucker-Management
- Schnellere Generierung ist Komfort (keine Notwendigkeit, aber nett)

**Langzeit-Abos (mit Rabatt):**
| Laufzeit | Preis | Rabatt | Pro Monat |
|----------|-------|--------|-----------|
| 1 Monat  | 2,99€ | -      | 2,99€     |
| 6 Monate | 15€   | 16%    | 2,50€     |
| 12 Monate| 29€   | 19%    | 2,42€     |

**Geschätzte Kosten pro User:** 0,80€/Monat (Hosting DB, APIs)
**Gewinnmarge:** 2,19€/User/Monat = **73%**

---

### **PREMIUM TIER** ⭐ - 4,99€/Monat
**Zielgruppe:** Diabetiker mit komplexen Bedürfnissen, Familien mit diabetischen Kindern

**Philosophie:** Meal-Planning + Zeitersparnis für Familien.

**Features:**
✅ **Alles aus BASIC Tier**
✅ **Erweiterte Rezept-DB:** 10.000 Rezepte
✅ **25x schnellere Generierung** (76s → 3s) ⚡⚡
✅ **Meal-Planning mit Kohlenhydrat-Budget** ⭐
✅ **Wochenplaner:** 7-Tage-Vorschau mit BE-Tracking ⭐
✅ **Saisonale Rezept-Empfehlungen**
✅ **Schritt-für-Schritt Foto-Guides**
✅ **Rezept-Skalierung** (1-12 Personen)
✅ **Allergen-Tracking** (wichtig bei Diabetiker + Allergien)
✅ **KI-Optimierung:** "Mach es diabetiker-freundlicher" (<10g KH)
✅ **Blutzucker-Impact-Prognose:** Vorhergesagter Anstieg basierend auf GI/GL

**Rezept-DB Inhalt (10.000 Rezepte):**
- 2.000 Low-Carb Rezepte (<20g KH)
- 1.500 Low-GI Rezepte (GI <55)
- 1.000 diabetiker-freundliche Desserts
- 1.000 Meal-Prep Rezepte (Wochenplanung)
- 800 glutenfrei/laktosefrei
- 1.200 vegetarisch/vegan
- 1.500 internationale Küche (italienisch, asiatisch, mediterran)
- 1.000 schnelle Gerichte (<30min)

**Performance:**
- 70% der Anfragen: Instant aus DB (<1s)
- 30% neue Kombinationen: 2-4s (KI mit DB-Kontext)
- **Durchschnitt: 3s** (25x schneller als FREE)

**Warum 4,99€?**
- Meal-Planning spart **3h pro Woche** (Wert: ~30€)
- Kohlenhydrat-Budget hilft bei Blutzucker-Management
- Für Familien mit diabetischen Kindern essentiell
- Immer noch **50% günstiger** als altes PRO-Tier (19,99€)

**Langzeit-Abos (mit Rabatt):**
| Laufzeit | Preis | Rabatt | Pro Monat |
|----------|-------|--------|-----------|
| 1 Monat  | 4,99€ | -      | 4,99€     |
| 6 Monate | 26€   | 13%    | 4,33€     |
| 12 Monate| 49€   | 18%    | 4,08€     |

**Geschätzte Kosten pro User:** 1,50€/Monat (Hosting, Nährwert-APIs)
**Gewinnmarge:** 3,49€/User/Monat = **70%**

---

### **PRO TIER** 🚀 - 9,99€/Monat
**Zielgruppe:** Ernährungsberater, Diabetologen, Diabetiker-Coaches, Profis

**Philosophie:** Für Profis, die mit der App Geld verdienen.

**Features:**
✅ **Alles aus PREMIUM Tier**
✅ **Maximale Rezept-DB:** 50.000+ Rezepte
✅ **38x schnellere Generierung** (76s → 2s) ⚡⚡⚡
✅ **API-Zugang** (für eigene Tools/Apps)
✅ **Team-Features:** Bis zu 5 Patienten/Klienten
✅ **Patienten-Management:** Individuelle Kohlenhydrat-Budgets ⭐
✅ **Export für Ärzte:** PDF-Reports mit Nährwert-Analysen
✅ **White-Label:** Eigenes Branding für Praxen
✅ **Custom Präferenzen:** Eigene Diät-Regeln (z.B. "Typ-1 Kind, 8 Jahre, 180g KH/Tag")
✅ **Insulin-Bedarfs-Rechner:** Basierend auf BE + individuellem Faktor
✅ **Prioritäts-Support:** 24h Response-Time

**Rezept-DB Inhalt (50.000+ Rezepte):**
- 10.000 Low-Carb Rezepte (alle Varianten)
- 5.000 Low-GI Rezepte
- 3.000 diabetiker-freundliche Desserts
- 5.000 Meal-Prep & Batch-Cooking
- 10.000 internationale Küchen (20+ Länder)
- 5.000 Diät-spezifisch (Keto, Paleo, DASH, etc.)
- 5.000 Restaurant-Rezepte
- 7.000 vegetarisch/vegan/glutenfrei/laktosefrei

**Performance:**
- 85% der Anfragen: Instant aus DB (<1s)
- 15% neue Kombinationen: 2-3s (KI mit DB-Kontext)
- **Durchschnitt: 2s** (38x schneller als FREE)
- API Response-Time: <500ms

**Warum 9,99€?**
- Ernährungsberater können damit **Geld verdienen**
- ROI: Spart **10h/Woche** = ~400€ Wert
- Team-Features für Patienten-Management
- White-Label für eigene Praxis-App

**Langzeit-Abos (mit Rabatt):**
| Laufzeit | Preis | Rabatt | Pro Monat |
|----------|-------|--------|-----------|
| 1 Monat  | 9,99€ | -      | 9,99€     |
| 6 Monate | 54€   | 10%    | 9,00€     |
| 12 Monate| 99€   | 17%    | 8,25€     |

**Geschätzte Kosten pro User:** 3€/Monat (Hosting, APIs, Support)
**Gewinnmarge:** 6,99€/User/Monat = **70%**

---

## 📊 Feature-Matrix (Diabetiker-fokussiert)

| Feature | FREE | BASIC | PREMIUM | PRO |
|---------|------|-------|---------|-----|
| **Preis** | 0€ | 2,99€ | 4,99€ | 9,99€ |
| **Rezept-DB** | ❌ | 1k | 10k | 50k+ |
| **Generierung** | 76s | 12s | 3s | 2s |
| **Basis-Nährwerte** | ✅ | ✅ | ✅ | ✅ |
| **Kohlenhydrate** | ✅ | ✅ | ✅ | ✅ |
| **Broteinheiten (BE)** | ✅ | ✅ | ✅ | ✅ |
| **Glykämischer Index (GI)** | ❌ | ✅ | ✅ | ✅ |
| **Glykämische Last (GL)** | ❌ | ✅ | ✅ | ✅ |
| **PDF-Export** | 10 max | ∞ | ∞ | ∞ |
| **Favoriten** | 10 | ∞ | ∞ | ∞ |
| **Sprachen** | 3 | 10 | 10 | 10 |
| **Meal-Planning** | ❌ | ❌ | ✅ | ✅ |
| **Kohlenhydrat-Budget** | ❌ | ❌ | ✅ | ✅ |
| **Wochenplaner** | ❌ | ❌ | ✅ | ✅ |
| **Diabetiker-Filter** | Basis | Erweitert | Erweitert | Erweitert |
| **Allergen-Tracking** | ❌ | ❌ | ✅ | ✅ |
| **Blutzucker-Prognose** | ❌ | ❌ | ✅ | ✅ |
| **Insulin-Rechner** | ❌ | ❌ | ❌ | ✅ |
| **API-Zugang** | ❌ | ❌ | ❌ | ✅ |
| **Team-Features** | ❌ | ❌ | ❌ | ✅ (5 User) |
| **Patienten-Management** | ❌ | ❌ | ❌ | ✅ |
| **White-Label** | ❌ | ❌ | ❌ | ✅ |
| **Support** | Community | Email | Priority | 24h |

---

## 🔧 Admin-Override (für dich als Entwickler/Diabetiker)

**Anforderung:** Du als Admin kannst alle Features kostenlos nutzen.

### Backend-Implementation:

```python
# backend/app/models/user.py
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    subscription_tier = Column(String, default="free")  # "free", "basic", "premium", "pro"
    is_admin = Column(Boolean, default=False)  # ⭐ Admin-Override
    created_at = Column(DateTime, default=datetime.utcnow)

# backend/app/services/subscription.py
def get_user_tier(user: User) -> str:
    """
    Returns effective subscription tier.
    Admins always get PRO-tier access.
    """
    if user.is_admin:
        return "pro"  # ⭐ Admin-Override: Immer PRO

    return user.subscription_tier

def check_feature_access(user: User, feature: str) -> bool:
    """
    Check if user has access to a specific feature.
    """
    tier = get_user_tier(user)  # Verwendet Admin-Override

    feature_tiers = {
        # FREE Features (kritisch für Diabetiker)
        "basic_nutrition": ["free", "basic", "premium", "pro"],
        "carbs_tracking": ["free", "basic", "premium", "pro"],
        "bread_units": ["free", "basic", "premium", "pro"],
        "pdf_export_limited": ["free"],
        "diabetic_filter_basic": ["free", "basic", "premium", "pro"],

        # BASIC Features
        "recipe_db_1k": ["basic", "premium", "pro"],
        "glycemic_index": ["basic", "premium", "pro"],
        "glycemic_load": ["basic", "premium", "pro"],
        "pdf_export_unlimited": ["basic", "premium", "pro"],
        "diabetic_filters_advanced": ["basic", "premium", "pro"],

        # PREMIUM Features
        "recipe_db_10k": ["premium", "pro"],
        "meal_planning": ["premium", "pro"],
        "carb_budget": ["premium", "pro"],
        "week_planner": ["premium", "pro"],
        "allergen_tracking": ["premium", "pro"],
        "blood_sugar_prediction": ["premium", "pro"],

        # PRO Features
        "recipe_db_50k": ["pro"],
        "api_access": ["pro"],
        "team_features": ["pro"],
        "patient_management": ["pro"],
        "insulin_calculator": ["pro"],
        "white_label": ["pro"],
    }

    allowed_tiers = feature_tiers.get(feature, [])
    return tier in allowed_tiers

# backend/app/routes/recipes.py
@router.post("/generate")
async def generate_recipe(
    ingredients: List[str],
    preferences: dict,
    current_user: User = Depends(get_current_user)
):
    # Check tier access (Admin gets "pro")
    tier = get_user_tier(current_user)

    # Select recipe DB based on tier
    if tier == "free":
        db_path = None  # No DB, only Ollama (76s)
    elif tier == "basic":
        db_path = "recipes_1k.db"  # 12s average
    elif tier == "premium":
        db_path = "recipes_10k.db"  # 3s average
    elif tier == "pro":
        db_path = "recipes_50k.db"  # 2s average

    # Generate recipe
    recipe = await recipe_service.generate(
        ingredients=ingredients,
        preferences=preferences,
        db_path=db_path
    )

    # Add nutrition (always available, even in FREE)
    if check_feature_access(current_user, "basic_nutrition"):
        recipe["nutrition"] = calculate_nutrition(recipe)
        recipe["bread_units"] = recipe["nutrition"]["carbs"] / 12

    # Add glycemic index (BASIC+)
    if check_feature_access(current_user, "glycemic_index"):
        recipe["glycemic_index"] = calculate_gi(recipe)
        recipe["glycemic_load"] = calculate_gl(recipe)

    # Add blood sugar prediction (PREMIUM+)
    if check_feature_access(current_user, "blood_sugar_prediction"):
        recipe["blood_sugar_impact"] = predict_blood_sugar_rise(
            gi=recipe["glycemic_index"],
            gl=recipe["glycemic_load"],
            carbs=recipe["nutrition"]["carbs"]
        )

    return recipe
```

**Admin-Setup:**
```sql
-- Setze dich selbst als Admin
UPDATE users SET is_admin = TRUE WHERE email = 'deine@email.com';
```

**Vorteil:**
- Admin-Check ist zentral an EINER Stelle (`get_user_tier()`)
- Alle Feature-Checks verwenden diese Funktion
- Du hast automatisch PRO-Zugriff (kostenlos)

---

## 🎯 Conversion-Strategie (Diabetiker-fokussiert)

### FREE → BASIC (Ziel: 20% Conversion)

**Trigger:**
- Nach 10 generierten Rezepten: "🚀 Warte 12s statt 76s! Upgrade zu BASIC."
- Nach 5 Favoriten: "💾 Speichere unbegrenzt viele Favoriten!"
- Wenn Nutzer Low-Carb sucht: "📊 Erhalte Glykämischen Index für bessere Blutzucker-Kontrolle!"

**Value Proposition:**
- "6x schneller für nur 2,99€/Monat (1x Kaffee)"
- "GI/GL für besseres Blutzucker-Management"
- "1.000 diabetiker-freundliche Rezepte"

---

### BASIC → PREMIUM (Ziel: 30% Conversion)

**Trigger:**
- Nach 50 Rezepten: "🍽️ Entdecke 10.000 weitere diabetiker-freundliche Rezepte!"
- Wenn Nutzer viele Favoriten hat: "📅 Meal-Planning spart dir 3h pro Woche!"
- Wenn Nutzer mehrmals Low-Carb wählt: "🎯 Wochenplaner mit Kohlenhydrat-Budget!"

**Value Proposition:**
- "10x mehr Rezepte für nur 2€ mehr"
- "Meal-Planning mit Kohlenhydrat-Budget (kritisch für Diabetiker!)"
- "25x schneller: 3s statt 76s"

---

### PREMIUM → PRO (Ziel: 5% Conversion)

**Trigger:**
- Wenn Nutzer >20 Rezepte/Woche generiert: "👨‍⚕️ Bist du Ernährungsberater?"
- Wenn Nutzer Team-Features nutzen könnte: "👥 Verwalte Patienten mit individuellem Kohlenhydrat-Budget!"
- Wenn Nutzer professionell wirkt: "💼 White-Label für deine Praxis!"

**Value Proposition:**
- "50.000+ Rezepte für alle Diabetiker-Typen"
- "API für eigene Apps/Tools"
- "ROI für Profis: Spart 10h/Woche = 400€"

---

## 📈 Umsatz-Prognose (12 Monate) - Diabetiker-fokussiert

**Annahmen (konservativ):**
- 15.000 FREE User nach 12 Monaten (viele Diabetiker)
- 20% Conversion zu BASIC (3.000 User)
- 30% von BASIC zu PREMIUM (900 User)
- 5% von PREMIUM zu PRO (45 User)

### Monatlicher Umsatz (Monat 12):
```
FREE:     15.000 User × 0€      = 0€
BASIC:     3.000 User × 2,99€   = 8.970€
PREMIUM:     900 User × 4,99€   = 4.491€
PRO:          45 User × 9,99€   = 450€
──────────────────────────────────────
GESAMT:                         13.911€/Monat
```

### Jahr 1 Gesamtumsatz:
```
~83.000€ (aufsteigend von 0€ in Monat 1)
```

### Jahr 2 Prognose (bei gleichbleibendem Wachstum):
```
~200.000€ (30.000 FREE, 6.000 BASIC, 1.800 PREMIUM, 90 PRO)
```

**Kosten (Monat 12 - Solo/mit Katja):**
```
Hosting (Hetzner/OCI):      ~50€/Monat
Nährwert-API:               ~10€/Monat
Stripe-Gebühren (1,4%):    ~250€/Monat
──────────────────────────────────────
GESAMT:                    ~310€/Monat
```

**Gewinn (Monat 12):**
```
Solo (100%):
13.911€ - 310€ = 13.601€/Monat (~163.200€/Jahr)

Mit Katja (50/50):
David:  6.801€/Monat (~81.600€/Jahr)
Katja:  6.801€/Monat (~81.600€/Jahr)
```

**Break-Even:** ~Monat 1-2 (bei nur 310€ Kosten!)

---

## 💡 Zusätzliche Monetarisierungs-Optionen (sozial vertretbar)

### 1. **Addon: Diabetiker-Rezept-Pakete** (Einmalzahlung)
```
"Diabetiker Starter Pack" - 200 Low-Carb Rezepte - 9,99€
"Typ-1 Kinder-Küche" - 150 kinderfreundliche Low-GI Rezepte - 7,99€
"Diabetiker Desserts" - 100 Zuckerersatz-Desserts - 6,99€
```

**Vorteil:** Einmalige Zahlung, permanenter Zugriff

---

### 2. **Affiliate-Partnerschaften (Diabetiker-fokussiert)**
- **Zuckerersatz:** Xucker, Erythrit, Stevia (5-10% Provision)
- **Kochbücher:** Diabetiker-Kochbücher bei Amazon
- **Blutzucker-Messgeräte:** FreeStyle Libre, Dexcom
- **Gesunde Lebensmittel:** REWE, Amazon Fresh (Bio-Produkte)

**Geschätzte Einnahmen:** 0,50-1,50€/User/Monat (BASIC+)

---

### 3. **Business-Lizenz** (für Diabetologen-Praxen)
```
Einzelpraxis (1-3 Ärzte):        49€/Monat
Gruppenpraxis (4-10 Ärzte):      99€/Monat
Klinik (10+ Ärzte):             299€/Monat
```

**Features:**
- Unbegrenzte Patienten
- Custom Rezept-Import (Praxis-eigene Rezepte)
- Export für Krankenakten
- White-Label mit Praxis-Logo

---

## 🏆 Erfolgs-Metriken

**KPIs zu tracken:**
1. **FREE → BASIC Conversion:** Ziel 20% (Diabetiker zahlen eher für GI/GL)
2. **BASIC → PREMIUM Conversion:** Ziel 30% (Meal-Planning ist wertvoll)
3. **Churn Rate:** Ziel <3%/Monat (Diabetiker bleiben langfristig)
4. **Average Revenue per User (ARPU):** Ziel 0,95€
5. **Lifetime Value (LTV):** Ziel 80€+ (langfristige Nutzung bei Diabetikern)
6. **Customer Acquisition Cost (CAC):** Budget <10€ (Mundpropaganda in Community)

---

## 🎯 Fazit & Empfehlung

### ✅ Soziale Mission erfüllt:
- **FREE hat ALLES Kritische:** Kohlenhydrate, BE, Basis-Nährwerte, PDF-Export
- Diabetiker können App vollständig kostenlos nutzen
- Keine Paywall für lebensnotwendige Features
- Admin (du) hat PRO-Zugriff kostenlos

### ✅ Nachhaltig finanziert:
- 2,99€ ist erschwinglich für ALLE (1x Kaffee)
- GI/GL + Speed rechtfertigen BASIC-Tier
- Meal-Planning in PREMIUM spart Zeit (3h/Woche)
- PRO-Tier für Profis hat klaren ROI (10h/Woche)

### ✅ Klare Differenzierung:
- FREE: Langsam (76s), aber funktional
- BASIC: Schnell (12s) + GI/GL
- PREMIUM: Sehr schnell (3s) + Meal-Planning
- PRO: Instant (2s) + Business-Tools

### ✅ Break-Even in 6-8 Monaten:
- Konservative Prognose: ~83.000€ Jahr 1
- Realistische Prognose: ~200.000€ Jahr 2
- Kosten: ~10.000€/Monat (Hosting, Support, Marketing)
- Gewinn Jahr 1: ~47.000€

---

## 🚀 Nächste Schritte

### Phase 1: Backend-Implementation (Monat 1-2)
1. User-Model: `is_admin`, `subscription_tier` hinzufügen
2. `get_user_tier()` + `check_feature_access()` implementieren
3. Nährwert-Berechnung (Kalorien, KH, Protein, Fett, Ballaststoffe)
4. BE-Berechnung (Kohlenhydrate ÷ 12)
5. Admin-Override testen (dich als Admin setzen)

### Phase 2: Rezept-DB + Tier-System (Monat 3-4)
1. Rezept-DB aufbauen (1k, 10k, 50k Rezepte)
2. Hybrid-Modus: DB + Ollama
3. GI/GL-Berechnung (BASIC+)
4. Performance-Tests (76s → 12s → 3s → 2s)

### Phase 3: Stripe-Integration (Monat 5-6)
1. Stripe-Account erstellen
2. Subscription-Management (monatlich, 6/12 Monate)
3. Webhooks für Payments
4. Upgrade/Downgrade-Flow

### Phase 4: Diabetiker-Features (Monat 7-9)
1. Meal-Planning (PREMIUM)
2. Wochenplaner mit Kohlenhydrat-Budget
3. Blutzucker-Impact-Prognose
4. Insulin-Rechner (PRO)

### Phase 5: Launch (Monat 10-12)
1. Beta-Tests mit Diabetiker-Community
2. Marketing (Diabetes-Foren, Facebook-Gruppen)
3. First 100 Paying Users
4. Feedback-Loop + Optimierungen

---

**Nächster Schritt:** Implementiere Admin-Override + Basis-Nährwerte im Backend! 🚀
