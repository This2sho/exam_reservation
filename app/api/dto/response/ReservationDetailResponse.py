from pydantic import BaseModel
from datetime import date, time

class ReservationDetailResponse(BaseModel):
    reservation_id: int
    date: date
    start_time: time
    end_time: time
    num_participants: int
    status: str
