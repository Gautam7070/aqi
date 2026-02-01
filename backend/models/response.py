from pydantic import BaseModel
from typing import Dict


class AQIResponse(BaseModel):
    city: str
    aqi: int
    components: Dict[str, float]
