from fastapi import APIRouter
from pydantic import BaseModel
router= APIRouter(prefix='')

# Pydantic response model for health check
class HealthCheckResponse(BaseModel):
    status: str

@router.get("/health",  response_model=HealthCheckResponse)
def health_check():
    return {"status": "healthy"}




