"""
Rate Limiting Middleware for Ollama AI Generation
- Limits concurrent requests to prevent Pi overload
- Queue system for excess requests
"""
import asyncio
import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)


class OllamaRateLimiter:
    """
    Simple rate limiter for Ollama requests
    - Max 2-3 concurrent requests
    - Queue system for waiting requests
    """

    def __init__(self, max_concurrent: int = 2):
        self.max_concurrent = max_concurrent
        self.current_requests = 0
        self.lock = asyncio.Lock()
        self.request_times: Dict[str, float] = {}  # Track request timing
        logger.info(f"OllamaRateLimiter initialized (max_concurrent: {max_concurrent})")

    async def acquire(self, request_id: str) -> bool:
        """
        Acquire permission to make a request
        Returns True if allowed, False if rate limited
        """
        async with self.lock:
            if self.current_requests < self.max_concurrent:
                self.current_requests += 1
                self.request_times[request_id] = time.time()
                logger.info(f"Request {request_id} acquired slot ({self.current_requests}/{self.max_concurrent})")
                return True
            else:
                logger.warning(f"Request {request_id} rate limited ({self.current_requests}/{self.max_concurrent})")
                return False

    async def release(self, request_id: str):
        """Release a request slot"""
        async with self.lock:
            if self.current_requests > 0:
                self.current_requests -= 1

                # Log duration
                if request_id in self.request_times:
                    duration = time.time() - self.request_times[request_id]
                    logger.info(f"Request {request_id} released slot (duration: {duration:.1f}s, remaining: {self.current_requests}/{self.max_concurrent})")
                    del self.request_times[request_id]


# Global rate limiter instance
ollama_limiter = OllamaRateLimiter(max_concurrent=2)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to rate limit AI generation endpoints
    Only applies to /recipes/generate* routes
    """

    async def dispatch(self, request: Request, call_next):
        # Check if this is an AI generation route
        path = request.url.path

        if path.startswith("/recipes/generate"):
            # Generate unique request ID
            request_id = f"{id(request)}-{time.time()}"

            # Try to acquire slot
            allowed = await ollama_limiter.acquire(request_id)

            if not allowed:
                # Rate limited - return 429
                return HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "rate_limit_exceeded",
                        "message": "Zu viele gleichzeitige Anfragen. Bitte warte kurz und versuche es erneut.",
                        "max_concurrent": ollama_limiter.max_concurrent,
                        "current": ollama_limiter.current_requests
                    }
                ).json()

            try:
                # Process request
                response = await call_next(request)
                return response
            finally:
                # Always release slot
                await ollama_limiter.release(request_id)

        else:
            # Not an AI route - pass through
            return await call_next(request)
