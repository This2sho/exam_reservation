from pydantic import BaseModel

class CreateReservationResponse(BaseModel):
    reservation_id: int  # 생성된 예약 ID
