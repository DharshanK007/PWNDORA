import os

filepath = "backend/app/main.py"
with open(filepath, "r") as f:
    content = f.read()

imports = '''from app.core.middleware import RequestIDMiddleware, SecurityHeadersMiddleware, RateLimitMiddleware
'''

if "RequestIDMiddleware" not in content:
    content = imports + content

# Add middlewares. Order matters.
# Security headers first, then RequestID, then RateLimit, then CORS.
# Actually in FastAPI, the last added middleware is the outermost.
# So we add CORSMiddleware, then RequestID, SecurityHeaders, RateLimit.

middlewares_code = '''
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
'''

if "RateLimitMiddleware" not in content:
    content = content.replace("app.add_middleware(\n    CORSMiddleware,", middlewares_code + "\napp.add_middleware(\n    CORSMiddleware,")

with open(filepath, "w") as f:
    f.write(content)

print("Added middlewares to main.py")
