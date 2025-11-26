from abc import ABC, abstractmethod

from src.domain.health import Health


class AbstractHealthRepository(ABC):
    """
    Abstract base class for a health repository.
    Defines the contract for fetching system health status.
    """

    @abstractmethod
    async def get_status(self) -> Health:
        """
        Retrieves the current health status of the system.
        """
        raise NotImplementedError