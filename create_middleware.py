content = '''from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid
import time
from app.core.config import settings

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

# Abstract RateLimiter interface
class RateLimiter:
    def is_allowed(self, client_ip: str) -> bool:
        raise NotImplementedError

# In-memory implementation
class InMemoryRateLimiter(RateLimiter):
    def __init__(self, limit: int, window: int = 60):
        self.limit = limit
        self.window = window
        self.clients = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        # Cleanup old requests
        self.clients[client_ip] = [t for t in self.clients[client_ip] if now - t < self.window]
        
        if len(self.clients[client_ip]) >= self.limit:
            return False
            
        self.clients[client_ip].append(now)
        return True

limiter = InMemoryRateLimiter(limit=settings.RATE_LIMIT_PER_MINUTE)

from fastapi.responses import JSONResponse
from fastapi import status

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        if not limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"success": False, "message": "Too many requests", "data": None, "metadata": {}}
            )
        return await call_next(request)
'''

with open("backend/app/core/middleware.py", "w") as f:
    f.write(content)
