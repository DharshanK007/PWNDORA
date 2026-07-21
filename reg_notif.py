api_file = "backend/app/api/v1/api.py"
with open(api_file, "r") as f:
    content = f.read()

if "from app.api.v1.endpoints import notifications" not in content:
    content = content.replace(
        "from app.api.v1.endpoints import audit", 
        "from app.api.v1.endpoints import audit\nfrom app.api.v1.endpoints import notifications"
    )
    content += '\napi_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])\n'
    with open(api_file, "w") as f:
        f.write(content)

print("Registered notifications endpoint.")
