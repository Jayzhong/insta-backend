from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from src.application.health.health_check import HealthCheckUseCase
from src.interfaces.api.dependencies import get_health_check_use_case


class HealthOut(BaseModel):
    """
    Pydantic schema for the health check API response.
    """
    status: str

    model_config = ConfigDict(from_attributes=True)


health_router = APIRouter()


@health_router.get("/health", tags=["Health"])
async def check_health(
    use_case: HealthCheckUseCase = Depends(get_health_check_use_case),
):
    """
    Endpoint to check the health of the application.
    It runs a use case that verifies connectivity to infrastructure services.
    """
    health_status = await use_case.execute()
    return health_status
