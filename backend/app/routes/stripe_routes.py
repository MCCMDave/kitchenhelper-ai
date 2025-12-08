"""
Stripe Integration - Subscription Management

Freemium Tiers:
- FREE: 0€
- BASIC: 2,99€/Monat
- PREMIUM: 4,99€/Monat
- PRO: 9,99€/Monat
- BUSINESS Solo: 19,99€/Monat
- BUSINESS Team: 39,99€/Monat
- BUSINESS Praxis: 79,99€/Monat
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.user import User, SubscriptionTier
from app.routes.auth import get_current_user
from app.config import settings
import stripe
import logging

logger = logging.getLogger(__name__)

# Stripe API Key (aus .env)
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")

router = APIRouter(prefix="/stripe", tags=["Stripe"])


# Stripe Price IDs (müssen in Stripe Dashboard erstellt werden)
PRICE_IDS = {
    "basic_monthly": "price_basic_monthly",  # 2,99€/Monat
    "basic_6months": "price_basic_6months",  # 15€/6 Monate
    "basic_yearly": "price_basic_yearly",    # 29€/Jahr

    "premium_monthly": "price_premium_monthly",  # 4,99€/Monat
    "premium_6months": "price_premium_6months",  # 26€/6 Monate
    "premium_yearly": "price_premium_yearly",    # 49€/Jahr

    "pro_monthly": "price_pro_monthly",  # 9,99€/Monat
    "pro_6months": "price_pro_6months",  # 54€/6 Monate
    "pro_yearly": "price_pro_yearly",    # 99€/Jahr

    "business_solo": "price_business_solo",  # 19,99€/Monat
    "business_team": "price_business_team",  # 39,99€/Monat
    "business_praxis": "price_business_praxis",  # 79,99€/Monat
}


@router.post("/create-checkout-session")
async def create_checkout_session(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Erstellt Stripe Checkout Session für Subscription

    Body:
    {
        "price_id": "price_basic_monthly",
        "success_url": "https://kitchenhelper-ai.de/success",
        "cancel_url": "https://kitchenhelper-ai.de/cancel"
    }
    """
    try:
        price_id = data.get("price_id")
        success_url = data.get("success_url", f"{settings.FRONTEND_URL}/settings?success=true")
        cancel_url = data.get("cancel_url", f"{settings.FRONTEND_URL}/settings?canceled=true")

        if not price_id or price_id not in PRICE_IDS.values():
            raise HTTPException(status_code=400, detail="Invalid price_id")

        # Stripe Customer erstellen (falls noch nicht vorhanden)
        if not current_user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                metadata={
                    "user_id": current_user.id,
                    "username": current_user.username,
                }
            )
            current_user.stripe_customer_id = customer.id
            db.commit()

        # Checkout Session erstellen
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=["card", "sepa_debit"],
            mode="subscription",
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "user_id": current_user.id,
            },
            allow_promotion_codes=True,  # Rabatt-Codes erlauben
        )

        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id,
        }

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Stripe Webhook Handler

    Events:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle Event
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "customer.subscription.created":
        await _handle_subscription_created(data, db)

    elif event_type == "customer.subscription.updated":
        await _handle_subscription_updated(data, db)

    elif event_type == "customer.subscription.deleted":
        await _handle_subscription_deleted(data, db)

    elif event_type == "invoice.payment_succeeded":
        logger.info(f"Payment succeeded: {data.get('id')}")

    elif event_type == "invoice.payment_failed":
        logger.warning(f"Payment failed: {data.get('id')}")
        await _handle_payment_failed(data, db)

    return {"status": "success"}


async def _handle_subscription_created(data: dict, db: Session):
    """Subscription erstellt"""
    customer_id = data.get("customer")
    price_id = data["items"]["data"][0]["price"]["id"]

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        logger.error(f"User not found for customer: {customer_id}")
        return

    # Setze Tier basierend auf Price ID
    tier = _get_tier_from_price_id(price_id)
    user.subscription_tier = tier
    db.commit()

    logger.info(f"Subscription created: {user.email} → {tier.value}")


async def _handle_subscription_updated(data: dict, db: Session):
    """Subscription aktualisiert (z.B. Upgrade/Downgrade)"""
    customer_id = data.get("customer")
    price_id = data["items"]["data"][0]["price"]["id"]

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        logger.error(f"User not found for customer: {customer_id}")
        return

    tier = _get_tier_from_price_id(price_id)
    user.subscription_tier = tier
    db.commit()

    logger.info(f"Subscription updated: {user.email} → {tier.value}")


async def _handle_subscription_deleted(data: dict, db: Session):
    """Subscription gekündigt"""
    customer_id = data.get("customer")

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        logger.error(f"User not found for customer: {customer_id}")
        return

    # Zurück zu FREE Tier
    user.subscription_tier = SubscriptionTier.FREE
    db.commit()

    logger.info(f"Subscription deleted: {user.email} → FREE")


async def _handle_payment_failed(data: dict, db: Session):
    """Zahlung fehlgeschlagen"""
    customer_id = data.get("customer")

    user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
    if not user:
        return

    # TODO: Email senden an User (Zahlung fehlgeschlagen)
    logger.warning(f"Payment failed for: {user.email}")


def _get_tier_from_price_id(price_id: str) -> SubscriptionTier:
    """Mapped Price ID zu Tier"""
    tier_map = {
        "price_basic_monthly": SubscriptionTier.BASIC,
        "price_basic_6months": SubscriptionTier.BASIC,
        "price_basic_yearly": SubscriptionTier.BASIC,

        "price_premium_monthly": SubscriptionTier.PREMIUM,
        "price_premium_6months": SubscriptionTier.PREMIUM,
        "price_premium_yearly": SubscriptionTier.PREMIUM,

        "price_pro_monthly": SubscriptionTier.PRO,
        "price_pro_6months": SubscriptionTier.PRO,
        "price_pro_yearly": SubscriptionTier.PRO,

        "price_business_solo": SubscriptionTier.BUSINESS_SOLO,
        "price_business_team": SubscriptionTier.BUSINESS_TEAM,
        "price_business_praxis": SubscriptionTier.BUSINESS_PRAXIS,
    }
    return tier_map.get(price_id, SubscriptionTier.FREE)


@router.get("/pricing")
async def get_pricing():
    """
    Gibt Pricing-Info zurück (öffentlich)
    """
    return {
        "tiers": [
            {
                "tier": "free",
                "name": "FREE",
                "price_monthly": 0,
                "features": [
                    "Unbegrenzte Rezept-Generierung (langsam, 76s)",
                    "10 Favoriten",
                    "Basis-Nährwerte (Kalorien, Kohlenhydrate, Protein, Fett)",
                    "BE-Berechnung",
                    "PDF-Export für Favoriten",
                ],
                "speed": "1x (76s)",
                "db_size": 0,
            },
            {
                "tier": "basic",
                "name": "BASIC",
                "price_monthly": 2.99,
                "price_6months": 15,
                "price_yearly": 29,
                "features": [
                    "6x schnellere Generierung (12s)",
                    "1.000 Rezepte Datenbank",
                    "Glykämischer Index (GI/GL)",
                    "Unbegrenzte Favoriten",
                    "Unbegrenzte PDF-Exporte",
                    "Einkaufslisten",
                ],
                "speed": "6x (12s)",
                "db_size": 1000,
                "price_ids": {
                    "monthly": "price_basic_monthly",
                    "6months": "price_basic_6months",
                    "yearly": "price_basic_yearly",
                },
            },
            {
                "tier": "premium",
                "name": "PREMIUM",
                "price_monthly": 4.99,
                "price_6months": 26,
                "price_yearly": 49,
                "features": [
                    "25x schnellere Generierung (3s)",
                    "10.000 Rezepte Datenbank",
                    "Meal-Planning",
                    "Kohlenhydrat-Budget",
                    "Erweiterte Filter",
                ],
                "speed": "25x (3s)",
                "db_size": 10000,
                "price_ids": {
                    "monthly": "price_premium_monthly",
                    "6months": "price_premium_6months",
                    "yearly": "price_premium_yearly",
                },
            },
            {
                "tier": "pro",
                "name": "PRO",
                "price_monthly": 9.99,
                "price_6months": 54,
                "price_yearly": 99,
                "features": [
                    "38x schnellere Generierung (2s)",
                    "50.000 Rezepte Datenbank",
                    "API-Zugang",
                    "Team-Sharing",
                    "White-Label",
                ],
                "speed": "38x (2s)",
                "db_size": 50000,
                "price_ids": {
                    "monthly": "price_pro_monthly",
                    "6months": "price_pro_6months",
                    "yearly": "price_pro_yearly",
                },
            },
        ]
    }


@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Kündigt aktive Subscription
    """
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No active subscription")

    try:
        # Hole aktive Subscriptions
        subscriptions = stripe.Subscription.list(
            customer=current_user.stripe_customer_id,
            status="active",
            limit=1
        )

        if not subscriptions.data:
            raise HTTPException(status_code=400, detail="No active subscription found")

        # Kündige Subscription (am Ende der Laufzeit)
        subscription = subscriptions.data[0]
        stripe.Subscription.modify(
            subscription.id,
            cancel_at_period_end=True
        )

        return {
            "message": "Subscription will be canceled at period end",
            "cancel_at": subscription.current_period_end,
        }

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
