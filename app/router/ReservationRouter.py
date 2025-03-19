from fastapi import APIRouter, Depends, status, Cookie
from sqlalchemy.orm import Session
from datetime import date

from app.database.database import get_db
from app.api.ReservationService import ReservationService
from app.api.dto.request.CreateReservationRequest import CreateReservationRequest
from app.api.dto.request.UpdateReservationRequest import UpdateReservationRequest
from app.api.dto.response.AdminReservationsResponse import AdminReservationsResponse
from app.api.dto.response.AvailableTimesResponse import AvailableTimesResponse
from app.api.dto.response.CreateReservationResponse import CreateReservationResponse
from app.api.dto.response.ReservationsResponse import ReservationsResponse

router = APIRouter()

@router.post("/reservations", response_model=CreateReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    request: CreateReservationRequest,
    db: Session = Depends(get_db),
    user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    return reservation_service.create_reservation(request, user_id)

@router.get("/reservations", response_model=ReservationsResponse)
def get_user_reservations(
    db: Session = Depends(get_db),
    user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    return reservation_service.find_reservations(user_id)

@router.get("/admin/reservations", response_model=AdminReservationsResponse)
def get_admin_reservations(
    db: Session = Depends(get_db),
    user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    return reservation_service.find_reservations_for_admin(user_id)

@router.get("/reservations/available-times", response_model=AvailableTimesResponse)
def get_available_times(
    reservation_date: date,
    db: Session = Depends(get_db)
):
    reservation_service = ReservationService(db)
    return reservation_service.find_available_reservations(reservation_date)

@router.put("/reservations/{reservation_id}", status_code=status.HTTP_200_OK)
def modify_reservation(
        reservation_id: int,
        request: UpdateReservationRequest,
        db: Session = Depends(get_db),
        user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    reservation_service.modify_reservation(user_id, reservation_id, request)
    return {"message": "예약이 수정되었습니다."}

@router.patch("/reservations/{reservation_id}/cancel", status_code=status.HTTP_200_OK)
def cancel_reservation(
        reservation_id: int,
        db: Session = Depends(get_db),
        user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    reservation_service.cancel_reservation(user_id, reservation_id)
    return {"message": "예약이 취소되었습니다."}

@router.patch("/reservations/{reservation_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_reservation(
        reservation_id: int,
        db: Session = Depends(get_db),
        user_id: int = Cookie(alias="X-User-ID", default=None)
):
    reservation_service = ReservationService(db)
    reservation_service.confirm_reservation(user_id, reservation_id)
    return {"message": "예약이 확정되었습니다."}
