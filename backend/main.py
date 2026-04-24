from fastapi import FastAPI
from api.router import router as api_router

app = FastAPI(
    title="LegaFlo Backend API",
    description="Agentic Orchestration and API endpoints for the LegaFlo Operating System",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LegaFlo Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
