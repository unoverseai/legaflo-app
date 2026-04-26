import os
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

# --- 1. ROUTER IMPORT ---
# This pulls in your endpoints like /translate and /chat
try:
    from api.router import router as api_router
except ImportError:
    # Fallback if the folder structure varies slightly in your IDE
    from .api.router import router as api_router

# --- 2. ENVIRONMENT & REQUIREMENTS ---
# List of keys LegaFlo needs to function as a Legal-Tech platform
REQUIRED_ENV_VARS = [
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "GEMINI_API_KEY",
    "DIGITAL_SCR_API_KEY",
    "DIGITAL_SCR_BASE_URL"
]

# Absolute pathing for .env loading
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug prints to confirm the fuel is in the tank
print(f"DEBUG: Loading .env from {env_path}")
print(f"DEBUG: GEMINI_API_KEY is {'Set' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")

# --- 3. LIFESPAN MANAGEMENT ---
# Checks for missing keys BEFORE the server opens to users
@asynccontextmanager
async def lifespan(app: FastAPI):
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        print(f"CRITICAL ERROR: {error_msg}")
        raise RuntimeError(error_msg)
    
    print("INFO: All environment variables verified. LegaFlo Intelligence is online.")
    yield

from fastapi.middleware.cors import CORSMiddleware

# --- 4. APP INITIALIZATION ---
app = FastAPI(
    title="LegaFlo Backend API",
    description="Agentic Orchestration and API endpoints for the LegaFlo Operating System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach the traffic controller
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LegaFlo Backend"}

# --- 5. SERVER LAUNCH ---
if __name__ == "__main__":
    import uvicorn
    config_host = os.getenv("HOST", "127.0.0.1")
    config_port = int(os.getenv("PORT", "8000"))
    # In development, use 'reload=True' to see changes instantly
    uvicorn.run("main:app", host=config_host, port=config_port, reload=True)