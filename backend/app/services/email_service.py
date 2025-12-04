"""
Email Service using Resend.com API

Handles all email operations:
- User registration verification
- Password reset
- Rate limiting (100 emails/day on Free Plan)
- Error handling with retry logic
- Email logging
"""

import os
import resend
import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from collections import deque
from functools import wraps
import time

# Logger setup
logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for Resend API (100 emails/day, 2 req/s)"""

    def __init__(self, max_daily: int = 100, max_per_second: int = 2):
        self.max_daily = max_daily
        self.max_per_second = max_per_second
        self.daily_requests = deque()
        self.second_requests = deque()

    def check_and_wait(self) -> bool:
        """
        Check rate limits and wait if needed
        Returns True if request can proceed
        """
        now = datetime.now()

        # Clean old daily requests (older than 24h)
        while self.daily_requests and (now - self.daily_requests[0]) > timedelta(hours=24):
            self.daily_requests.popleft()

        # Clean old per-second requests (older than 1s)
        while self.second_requests and (now - self.second_requests[0]) > timedelta(seconds=1):
            self.second_requests.popleft()

        # Check daily limit
        if len(self.daily_requests) >= self.max_daily:
            logger.warning("Daily email limit reached (100/day)")
            return False

        # Check per-second limit
        if len(self.second_requests) >= self.max_per_second:
            wait_time = 0.5  # Wait 500ms to avoid hitting limit
            logger.info(f"Rate limit approaching, waiting {wait_time}s...")
            time.sleep(wait_time)

        # Record this request
        self.daily_requests.append(now)
        self.second_requests.append(now)
        return True


def retry_on_failure(max_retries: int = 3, delay: int = 5):
    """Decorator for automatic retry on temporary failures"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_msg = str(e).lower()
                    if ("rate limit" in error_msg or "timeout" in error_msg) and attempt < max_retries - 1:
                        wait_time = delay * (attempt + 1)  # Exponential backoff
                        logger.warning(f"Retry attempt {attempt + 1}/{max_retries} after {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e
            return None
        return wrapper
    return decorator


class EmailService:
    """
    Email service using Resend.com

    Features:
    - Rate limiting (100/day, 2/s)
    - Automatic retry on failures
    - Email logging
    - HTML templates support
    """

    def __init__(self, api_key: Optional[str] = None, from_email: Optional[str] = None):
        """
        Initialize email service

        Args:
            api_key: Resend API key (defaults to env RESEND_API_KEY)
            from_email: Default sender email (defaults to env RESEND_FROM_EMAIL)
        """
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        self.from_email = from_email or os.getenv("RESEND_FROM_EMAIL", "KitchenHelper <noreply@yourdomain.com>")

        if not self.api_key:
            raise ValueError("RESEND_API_KEY not found in environment variables")

        # Set Resend API key
        resend.api_key = self.api_key

        # Rate limiter
        self.rate_limiter = RateLimiter()

        logger.info("Email service initialized")

    @retry_on_failure(max_retries=3, delay=5)
    def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        text: Optional[str] = None,
        reply_to: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None
    ) -> Dict:
        """
        Send an email

        Args:
            to: Recipient email address
            subject: Email subject
            html: HTML content
            text: Plain text fallback (optional)
            reply_to: Reply-to address (optional)
            tags: List of tags for categorization

        Returns:
            Dict with email_id and success status

        Raises:
            Exception if sending fails after retries
        """
        # Check rate limit
        if not self.rate_limiter.check_and_wait():
            raise Exception("Daily email limit reached (100/day)")

        # Prepare params
        params: resend.Emails.SendParams = {
            "from": self.from_email,
            "to": [to],
            "subject": subject,
            "html": html,
        }

        if text:
            params["text"] = text

        if reply_to:
            params["reply_to"] = reply_to

        if tags:
            params["tags"] = tags

        try:
            # Send email
            logger.info(f"Sending email to {to} - Subject: {subject}")
            response = resend.Emails.send(params)

            email_id = response.get("id")
            logger.info(f"Email sent successfully - ID: {email_id}")

            return {
                "success": True,
                "email_id": email_id,
                "recipient": to
            }

        except Exception as e:
            logger.error(f"Failed to send email to {to} - Error: {str(e)}")
            raise

    def send_verification_email(
        self,
        to: str,
        verification_url: str,
        user_name: Optional[str] = None
    ) -> Dict:
        """
        Send email verification link

        Args:
            to: User email address
            verification_url: Full verification URL with token
            user_name: User's name (optional)

        Returns:
            Dict with email_id and success status
        """
        greeting = f"Hallo {user_name}" if user_name else "Hallo"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #667eea;
                    color: white;
                    padding: 14px 28px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .button:hover {{
                    background-color: #5568d3;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
                .link {{
                    color: #667eea;
                    word-break: break-all;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🍳 KitchenHelper-AI</h1>
                </div>
                <div class="content">
                    <h2>{greeting}!</h2>
                    <p>Willkommen bei KitchenHelper-AI! Wir freuen uns, dich an Bord zu haben.</p>
                    <p>Bitte verifiziere deine E-Mail-Adresse, um deinen Account zu aktivieren:</p>
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">E-Mail verifizieren</a>
                    </div>
                    <p style="margin-top: 30px; font-size: 13px; color: #666;">
                        Oder kopiere diesen Link in deinen Browser:<br>
                        <span class="link">{verification_url}</span>
                    </p>
                    <p style="margin-top: 30px; font-size: 12px; color: #999;">
                        <strong>Hinweis:</strong> Dieser Link ist 24 Stunden gültig.
                    </p>
                </div>
                <div class="footer">
                    <p>Du hast diese E-Mail erhalten, weil du dich bei KitchenHelper-AI registriert hast.</p>
                    <p>Falls du diese Registrierung nicht vorgenommen hast, ignoriere diese E-Mail einfach.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        {greeting}!

        Willkommen bei KitchenHelper-AI! Wir freuen uns, dich an Bord zu haben.

        Bitte verifiziere deine E-Mail-Adresse, um deinen Account zu aktivieren:
        {verification_url}

        Dieser Link ist 24 Stunden gültig.

        Falls du diese Registrierung nicht vorgenommen hast, ignoriere diese E-Mail einfach.

        ---
        KitchenHelper-AI Team
        """

        # Get reply_to from env
        from app.config import settings

        return self.send_email(
            to=to,
            subject="Verifiziere deine E-Mail-Adresse - KitchenHelper-AI",
            html=html_content,
            text=text_content,
            reply_to=settings.RESEND_REPLY_TO,
            tags=[
                {"name": "type", "value": "verification"},
                {"name": "project", "value": "kitchenhelper"}
            ]
        )

    def send_password_reset_email(
        self,
        to: str,
        reset_url: str,
        user_name: Optional[str] = None
    ) -> Dict:
        """
        Send password reset link

        Args:
            to: User email address
            reset_url: Full password reset URL with token
            user_name: User's name (optional)

        Returns:
            Dict with email_id and success status
        """
        greeting = f"Hallo {user_name}" if user_name else "Hallo"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 30px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #f5576c;
                    color: white;
                    padding: 14px 28px;
                    text-decoration: none;
                    border-radius: 6px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .button:hover {{
                    background-color: #e0405a;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }}
                .link {{
                    color: #f5576c;
                    word-break: break-all;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Passwort zurücksetzen</h1>
                </div>
                <div class="content">
                    <h2>{greeting},</h2>
                    <p>Du hast einen Passwort-Reset für deinen KitchenHelper-AI Account angefordert.</p>
                    <p>Klicke auf den Button, um ein neues Passwort zu vergeben:</p>
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Passwort zurücksetzen</a>
                    </div>
                    <p style="margin-top: 30px; font-size: 13px; color: #666;">
                        Oder kopiere diesen Link in deinen Browser:<br>
                        <span class="link">{reset_url}</span>
                    </p>
                    <div class="warning">
                        <strong>⚠️ Sicherheitshinweis:</strong><br>
                        Falls du diese Anfrage nicht gestellt hast, ignoriere diese E-Mail.
                        Dein Passwort bleibt dann unverändert.
                    </div>
                    <p style="margin-top: 20px; font-size: 12px; color: #999;">
                        <strong>Hinweis:</strong> Dieser Link ist 24 Stunden gültig.
                    </p>
                </div>
                <div class="footer">
                    <p>KitchenHelper-AI - Dein smarter Küchenassistent</p>
                    <p>Diese E-Mail wurde automatisch generiert.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        {greeting},

        Du hast einen Passwort-Reset für deinen KitchenHelper-AI Account angefordert.

        Klicke auf den folgenden Link, um ein neues Passwort zu vergeben:
        {reset_url}

        ⚠️ SICHERHEITSHINWEIS:
        Falls du diese Anfrage nicht gestellt hast, ignoriere diese E-Mail.
        Dein Passwort bleibt dann unverändert.

        Dieser Link ist 24 Stunden gültig.

        ---
        KitchenHelper-AI Team
        """

        # Get reply_to from env
        from app.config import settings

        return self.send_email(
            to=to,
            subject="Passwort zurücksetzen - KitchenHelper-AI",
            html=html_content,
            text=text_content,
            reply_to=settings.RESEND_REPLY_TO,
            tags=[
                {"name": "type", "value": "password_reset"},
                {"name": "project", "value": "kitchenhelper"}
            ]
        )
