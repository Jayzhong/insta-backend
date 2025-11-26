from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Follow:
    """
    The Follow relationship entity.
    Represents 'follower' following 'followed'.
    """
    follower_id: UUID
    followed_id: UUID
    created_at: datetime = field(default_factory=datetime.now)
