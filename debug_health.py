from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass

@dataclass(frozen=True)
class Health:
    status: str

class HealthOut(BaseModel):
    status: str
    model_config = ConfigDict(from_attributes=True)

try:
    h = Health(status="ok")
    ho = HealthOut.model_validate(h)
    print(f"Validation success: {ho}")
except Exception as e:
    print(f"Validation failed: {e}")

print(f"HealthOut fields: {HealthOut.model_fields}")
