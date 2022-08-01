from fastapi import status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from routers.user import router as userRouter
from routers.stock import router as stockRouter

router = APIRouter()

router.include_router(userRouter, prefix="/user")
router.include_router(stockRouter, prefix="/stock")

class HealthCheck(BaseModel):
    title: str = Field(..., description="API title")
    description: str = Field(..., description="Brief description of the API")
    version: str = Field(..., description="API server version number")
    status: str = Field(..., description="API current status")

@router.get(
    "/status",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    return {
        "title": "ThndrTask",
        "description": "This is a test desc",
        "version": "0.0.0",
        "status": "OK",
    }