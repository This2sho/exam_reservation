from typing import List

from pydantic import BaseModel
from app.api.dto.response.AdminReservationDetailResponse import AdminReservationDetailResponse


class AdminReservationsResponse(BaseModel):
    reservations: List[AdminReservationDetailResponse]