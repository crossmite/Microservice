from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional



class TicketModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    passenger_name: str
    passport: str
    id_ship: int
    direction: str