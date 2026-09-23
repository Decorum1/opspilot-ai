from fastapi import FastAPI

app = FastAPI(
    title="OpsPilot AI",
    description="Intelligent Operations and Predictive Maintenance Platform",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpsPilot API"
    }
