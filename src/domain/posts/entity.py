from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class Post:
    """
    The Post aggregate root entity.
    """
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    image_url: str
    caption: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
