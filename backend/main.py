import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.router import router as api_router

REQUIRED_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "OPENAI_API_KEY",
    "DIGITAL_SCR_API_KEY",
    "DIGITAL_SCR_BASE_URL",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")
    yield

app = FastAPI(
    title="LegaFlo Backend API",
    description="Agentic Orchestration and API endpoints for the LegaFlo Operating System",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LegaFlo Backend"}

if __name__ == "__main__":
    import uvicorn
    config_host = os.getenv("HOST", "0.0.0.0")
    config_port = int(os.getenv("PORT", "8000"))
    config_reload = os.getenv("ENVIRONMENT", "production").lower() in ("development", "dev")
    uvicorn.run("main:app", host=config_host, port=config_port, reload=config_reload)
