from dataclasses import dataclass


@dataclass(frozen=True)
class Health:
    """
    Represents the health status of the system.
    """
    status: str