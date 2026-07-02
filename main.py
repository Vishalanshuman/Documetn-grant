from fastapi import FastAPI
from app.api.grants import router as grants_router


app = FastAPI(
    title="Document Grant Service",
    description="A service to manage document access grants.",
    version="0.1.0",
)

app.include_router(grants_router, prefix="/api/v1", tags=["grants"])

@app.get("/health")
def health_check():
    return {"status": "ok"}