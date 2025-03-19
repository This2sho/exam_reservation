from pydantic import BaseModel
from datetime import date, time


class UpdateReservationRequest(BaseModel):
    date: date
    start_time: time
    end_time: time
    num_participants: int