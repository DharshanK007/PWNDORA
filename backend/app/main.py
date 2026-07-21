from app.core.middleware import RequestIDMiddleware, SecurityHeadersMiddleware, RateLimitMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.exceptions import (
    NeoFactoryException,
    neofactory_exception_handler,
    global_exception_handler
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise API for NeoFactory Operations Platform",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(NeoFactoryException, neofactory_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include Routers
app.include_router(api_router, prefix=settings.API_V1_STR)



@app.on_event("startup")
def startup_event():
    import os
    from app.scenarios.scenario_manager import manager
    data_dir = os.path.join(os.path.dirname(__file__), "scenario_data")
    manager.load_all(data_dir)
    print(f"Loaded {len(manager.registry.list_scenarios())} scenarios")
