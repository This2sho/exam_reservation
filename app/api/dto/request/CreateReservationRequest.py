from pydantic import BaseModel
from datetime import date, time

class CreateReservationRequest(BaseModel):
    reservation_date: date
    num_participants: int
    start_time: time
    end_time: time