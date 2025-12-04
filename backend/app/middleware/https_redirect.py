"""
HTTPS Redirect Middleware
Forces HTTPS in production (except localhost/Tailscale)
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
import os


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce HTTPS in production

    - Redirects HTTP to HTTPS (301 Permanent)
    - Allows HTTP for: localhost, 127.0.0.1, 192.168.*, 100.* (Tailscale)
    - Disabled in DEBUG mode (for local development)
    """

    # Hosts that are allowed to use HTTP
    ALLOWED_HTTP_HOSTS = [
        "localhost",
        "127.0.0.1",
        "::1",
    ]

    def _is_local_network(self, host: str) -> bool:
        """Check if host is in local network (192.168.* or 100.* for Tailscale)"""
        return (
            host.startswith("192.168.") or
            host.startswith("10.") or
            host.startswith("172.") or
            host.startswith("100.")  # Tailscale CGNAT range
        )

    async def dispatch(self, request: Request, call_next):
        # Skip in DEBUG mode (local development)
        if os.getenv("DEBUG", "False").lower() == "true":
            return await call_next(request)

        # Already HTTPS? Continue
        if request.url.scheme == "https":
            return await call_next(request)

        # Get host from request
        host = request.url.hostname or ""

        # Allow HTTP for localhost and local networks
        if host in self.ALLOWED_HTTP_HOSTS or self._is_local_network(host):
            return await call_next(request)

        # Production: Redirect HTTP → HTTPS
        https_url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(https_url), status_code=301)
