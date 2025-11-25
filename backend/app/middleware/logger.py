# API Request Logger Middleware
# Logs all API requests to file for debugging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import time
import os


class APIRequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all API requests

    Logs:
    - Timestamp
    - Method
    - Path
    - Status Code
    - Duration (ms)
    - Client IP
    """

    def __init__(self, app, log_file="logs/api-requests.log"):
        super().__init__(app)
        self.log_file = log_file

        # Ensure logs directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = round((time.time() - start_time) * 1000, 2)

        # Format log entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[{timestamp}] "
            f"{request.method} "
            f"{request.url.path} "
            f"| Status: {response.status_code} "
            f"| Duration: {duration_ms}ms "
            f"| IP: {client_ip}"
        )

        # Write to file (append mode)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"[Logger] Error writing to log file: {e}")

        # Also print to console in debug mode
        if os.getenv("DEBUG", "False").lower() == "true":
            print(log_entry)

        return response
