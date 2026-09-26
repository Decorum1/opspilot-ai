from fastapi import FastAPI

import models
from database import engine
from routers import equipment


# Create database tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="OpsPilot AI",
    description="Intelligent Operations and Predictive Maintenance Platform",
    version="0.1.0"
)


# Register application routers
app.include_router(equipment.router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpsPilot API"
    }
