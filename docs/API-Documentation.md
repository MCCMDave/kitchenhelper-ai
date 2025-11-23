# KitchenHelper-AI API Documentation

**Base URL:** `https://api.kitchenhelper-ai.com/v1`  
**Version:** 1.0.0  
**Authentication:** JWT Bearer Token

---

## Authentication

### POST /auth/register
Neuen User registrieren

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Max Mustermann"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Max Mustermann",
  "subscription_tier": "demo",
  "created_at": "2025-11-21T10:00:00Z",
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

---

### POST /auth/login
User einloggen

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### POST /auth/refresh
Access Token erneuern

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "expires_in": 1800
}
```

---

## Users

### GET /users/me
Eigenes Profil abrufen

**Headers:** `Authorization: Bearer {token}`

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Max Mustermann",
  "subscription_tier": "basic",
  "daily_recipe_count": 5,
  "daily_limit": 50,
  "diet_profiles": ["diabetic", "vegan"],
  "created_at": "2025-11-21T10:00:00Z"
}
```

---

### PATCH /users/me
Profil aktualisieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "name": "Neuer Name",
  "email": "neue@email.com"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "neue@email.com",
  "name": "Neuer Name",
  "updated_at": "2025-11-21T11:00:00Z"
}
```

---

### DELETE /users/me
Account löschen (GDPR)

**Headers:** `Authorization: Bearer {token}`

**Response (204):** No Content

---

## Ingredients

### GET /ingredients
Alle Zutaten abrufen

**Headers:** `Authorization: Bearer {token}`

**Query Parameters:**
- `category` (optional): Filter nach Kategorie
- `expired` (optional): `true`/`false` - Nur abgelaufene/nicht abgelaufene

**Response (200):**
```json
{
  "ingredients": [
    {
      "id": "uuid",
      "name": "Tomaten",
      "category": "Gemüse",
      "expiry_date": "2025-11-25",
      "is_permanent": false,
      "added_at": "2025-11-20T10:00:00Z"
    },
    {
      "id": "uuid",
      "name": "Salz",
      "category": "Gewürze",
      "expiry_date": null,
      "is_permanent": true,
      "added_at": "2025-11-20T10:00:00Z"
    }
  ],
  "count": 2
}
```

---

### POST /ingredients
Neue Zutat hinzufügen

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "name": "Tomaten",
  "category": "Gemüse",
  "expiry_date": "2025-11-25",
  "is_permanent": false
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "name": "Tomaten",
  "category": "Gemüse",
  "expiry_date": "2025-11-25",
  "is_permanent": false,
  "added_at": "2025-11-21T10:00:00Z"
}
```

---

### PATCH /ingredients/{id}
Zutat aktualisieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "expiry_date": "2025-11-30"
}
```

**Response (200):** Updated ingredient object

---

### DELETE /ingredients/{id}
Zutat löschen

**Headers:** `Authorization: Bearer {token}`

**Response (204):** No Content

---

## Recipes

### POST /recipes/generate
KI-Rezepte generieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "ingredient_ids": ["uuid1", "uuid2", "uuid3"],
  "ai_provider": "anthropic",
  "diet_profiles": ["diabetic", "vegan"],
  "diabetes_unit": "KE"
}
```

**Response (200):**
```json
{
  "recipes": [
    {
      "id": "uuid",
      "name": "Mediterrane Tomaten-Pasta",
      "description": "Frische Tomaten mit Basilikum und Olivenöl...",
      "difficulty": 2,
      "cooking_time": "25 Min",
      "method": "Pfanne",
      "servings": 2,
      "used_ingredients": ["Tomaten", "Nudeln", "Olivenöl"],
      "leftover_tips": "Übrige Tomaten für Salat verwenden",
      "ingredients": [
        {
          "name": "Vollkornnudeln",
          "amount": "200g",
          "carbs": 60
        },
        {
          "name": "Tomaten",
          "amount": "300g",
          "carbs": 9
        }
      ],
      "nutrition_per_serving": {
        "calories": 350,
        "protein": 15,
        "carbs": 34.5,
        "fat": 12,
        "ke": 3.5
      },
      "generated_at": "2025-11-21T10:00:00Z",
      "ai_provider": "anthropic"
    }
  ],
  "count": 3,
  "daily_count_remaining": 47
}
```

**Error (429 - Rate Limit):**
```json
{
  "error": "daily_limit_reached",
  "message": "Tageslimit erreicht. Upgrade auf Basic für 50 Rezepte/Tag.",
  "daily_limit": 3,
  "subscription_tier": "demo",
  "upgrade_url": "/payments/upgrade"
}
```

---

### GET /recipes/history
Generierungs-Historie abrufen

**Headers:** `Authorization: Bearer {token}`

**Query Parameters:**
- `limit` (default: 20): Anzahl Ergebnisse
- `offset` (default: 0): Pagination
- `from_date` (optional): ISO timestamp
- `to_date` (optional): ISO timestamp

**Response (200):**
```json
{
  "recipes": [...],
  "total": 156,
  "limit": 20,
  "offset": 0
}
```

---

### GET /recipes/{id}
Einzelnes Rezept abrufen

**Headers:** `Authorization: Bearer {token}`

**Response (200):** Single recipe object

---

## Favorites

### GET /favorites
Alle Favoriten abrufen

**Headers:** `Authorization: Bearer {token}`

**Response (200):**
```json
{
  "favorites": [
    {
      "id": "uuid",
      "recipe": {...},
      "added_at": "2025-11-20T10:00:00Z"
    }
  ],
  "count": 12
}
```

---

### POST /favorites
Rezept als Favorit markieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "recipe_id": "uuid"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "recipe_id": "uuid",
  "added_at": "2025-11-21T10:00:00Z"
}
```

---

### DELETE /favorites/{id}
Favorit entfernen

**Headers:** `Authorization: Bearer {token}`

**Response (204):** No Content

---

## Diet Profiles

### GET /profiles
Aktive Ernährungsprofile abrufen

**Headers:** `Authorization: Bearer {token}`

**Response (200):**
```json
{
  "profiles": [
    {
      "id": "uuid",
      "type": "diabetic",
      "name": "Diabetes Typ 2",
      "settings": {
        "unit": "KE",
        "daily_carb_limit": 180
      },
      "is_active": true
    }
  ]
}
```

---

### POST /profiles
Ernährungsprofil aktivieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "type": "diabetic",
  "settings": {
    "unit": "KE",
    "daily_carb_limit": 180
  }
}
```

**Response (201):** Profile object

---

### PATCH /profiles/{id}
Profil-Einstellungen aktualisieren

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "settings": {
    "unit": "BE",
    "daily_carb_limit": 200
  }
}
```

**Response (200):** Updated profile object

---

### DELETE /profiles/{id}
Profil deaktivieren

**Headers:** `Authorization: Bearer {token}`

**Response (204):** No Content

---

## Payments

### POST /payments/create-checkout
Stripe Checkout Session erstellen

**Headers:** `Authorization: Bearer {token}`

**Request:**
```json
{
  "tier": "basic",
  "billing_interval": "monthly"
}
```

**Response (200):**
```json
{
  "checkout_url": "https://checkout.stripe.com/...",
  "session_id": "cs_..."
}
```

---

### POST /payments/webhook
Stripe Webhook Endpoint (intern)

**Headers:** `Stripe-Signature: {signature}`

**Request:** Stripe Event Payload

**Response (200):**
```json
{
  "received": true
}
```

---

### GET /payments/subscription-status
Abo-Status prüfen

**Headers:** `Authorization: Bearer {token}`

**Response (200):**
```json
{
  "tier": "basic",
  "status": "active",
  "current_period_end": "2025-12-21T10:00:00Z",
  "cancel_at_period_end": false
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": {
    "field": "email",
    "issue": "Invalid email format"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Try again in 60 seconds.",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limits

| Tier | Recipes/Day | API Calls/Min | Favorites |
|------|-------------|---------------|-----------|
| Demo | 3 | 10 | 5 |
| Basic | 50 | 60 | 50 |
| Premium | ∞ | 120 | ∞ |

---

## Webhooks

### Stripe Events
Die App hört auf folgende Stripe Events:
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`

---

**Letzte Aktualisierung:** November 2025  
**API Version:** 1.0.0
