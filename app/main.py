from fastapi import FastAPI

from app.routes import auth
from app.routes import plans
from app.routes import ai_tools
from app.routes import ai_requests
from app.routes import subscriptions
from app.routes import usage
from app.routes import api_keys
from app.routes import admin


app = FastAPI(
    title="AI SaaS Backend API",
    description="AI SaaS Backend for Sqrock IT Solutions Phase 2",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(plans.router)
app.include_router(ai_tools.router)
app.include_router(ai_requests.router)
app.include_router(subscriptions.router)
app.include_router(usage.router)
app.include_router(api_keys.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "message": "AI SaaS Backend API is running"
    }