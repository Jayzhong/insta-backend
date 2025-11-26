from src.application.health.health_repository import AbstractHealthRepository
from src.domain.health import Health


class DummyHealthRepository(AbstractHealthRepository):
    """
    A dummy implementation of the AbstractHealthRepository for infrastructure layer.
    It always returns a hardcoded "ok" status, simulating a successful health check.
    """

    async def get_status(self) -> Health:
        """
        Simulates retrieving the current health status of the system.
        Returns a hardcoded Health object with status "ok".
        """
        return Health(status="ok")