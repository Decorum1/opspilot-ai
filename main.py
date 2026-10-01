from fastapi import FastAPI

from routers import equipment, maintenance



app = FastAPI(
    title="OpsPilot AI",
    description="Intelligent Operations and Predictive Maintenance Platform",
    version="0.1.0"
)


app.include_router(equipment.router)
app.include_router(maintenance.router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpsPilot API"
    }
