from datetime import time

from pydantic import BaseModel


class AvailableSlotResponse(BaseModel):
    start_time: time
    end_time: time
    available_spots: int
