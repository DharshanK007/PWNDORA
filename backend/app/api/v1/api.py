from fastapi import APIRouter
from app.scenarios import scenario_router
from app.api.v1.endpoints import (
    dashboard,
    company,
    health,
    auth,
    users,
    employees,
    departments,
    devices,
    firmwares,
    locations,
    tickets,
    inventory,
    notifications,
    reports,
    activity_logs,
    audit,
    timeline,
    progress,
    attack_graph,
    report_drafts,
    analytics
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(firmwares.router, prefix="/firmwares", tags=["firmwares"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(activity_logs.router, prefix="/activity_logs", tags=["activity_logs"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(attack_graph.router, prefix="/attack-graph", tags=["attack_graph"])
api_router.include_router(report_drafts.router, prefix="/reports/draft", tags=["report_drafts"])
from app.api.v1.endpoints import search
api_router.include_router(search.router, prefix="/search", tags=["search"])

api_router.include_router(health.router, prefix="/health", tags=["health"])

api_router.include_router(company.router, prefix="/company", tags=["company"])

from app.api.v1.endpoints import scenarios as endpoints_scenarios
api_router.include_router(endpoints_scenarios.router, prefix="/scenarios", tags=["scenarios"])

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

