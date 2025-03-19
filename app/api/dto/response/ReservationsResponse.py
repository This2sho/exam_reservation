from typing import List

from pydantic import BaseModel
from app.api.dto.response.ReservationDetailResponse import ReservationDetailResponse

class ReservationsResponse(BaseModel):
    reservations: List[ReservationDetailResponse]