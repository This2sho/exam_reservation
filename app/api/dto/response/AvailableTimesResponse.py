from pydantic import BaseModel
from datetime import date
from app.api.dto.response.AvailableSlotResponse import AvailableSlotResponse


class AvailableTimesResponse(BaseModel):
    date: date
    available_slots: list[AvailableSlotResponse]
    