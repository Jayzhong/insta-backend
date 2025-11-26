from src.application.health.health_repository import AbstractHealthRepository
from src.domain.health import Health


class HealthCheckUseCase:
    """
    Use case for performing a health check of the system.
    Orchestrates the retrieval of health status using an abstract repository.
    """

    def __init__(self, health_repo: AbstractHealthRepository) -> None:
        """
        Initializes the HealthCheckUseCase with an abstract health repository.

        Args:
            health_repo: An instance of AbstractHealthRepository for data access.
        """
        self._health_repo: AbstractHealthRepository = health_repo

    async def execute(self) -> Health:
        """
        Executes the health check operation.

        Returns:
            A Health object indicating the system's current status.
        """
        return await self._health_repo.get_status()