from fastapi import APIRouter, Depends, status
from datetime import date

from app.api.AuthService import AuthService
from app.api.ReservationService import ReservationService
from app.api.dto.request.CreateReservationRequest import CreateReservationRequest
from app.api.dto.request.UpdateReservationRequest import UpdateReservationRequest
from app.api.dto.response.AdminReservationsResponse import AdminReservationsResponse
from app.api.dto.response.AvailableTimesResponse import AvailableTimesResponse
from app.api.dto.response.CreateReservationResponse import CreateReservationResponse
from app.api.dto.response.ReservationsResponse import ReservationsResponse
from app.domain.User import User

router = APIRouter(dependencies=[Depends(ReservationService)])
auth_service = AuthService()

@router.post("/reservations", response_model=CreateReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    request: CreateReservationRequest,
    user: User = Depends(auth_service.get_current_user),
    reservation_service: ReservationService = Depends()
):
    return reservation_service.create_reservation(request, user.id)

@router.get("/reservations", response_model=ReservationsResponse)
def get_user_reservations(
    user: User = Depends(auth_service.get_current_user),
    reservation_service: ReservationService = Depends()
):
    return reservation_service.find_reservations(user.id)

@router.get("/admin/reservations", response_model=AdminReservationsResponse)
def get_admin_reservations(
    user: User = Depends(auth_service.get_current_user),
    reservation_service: ReservationService = Depends()
):
    return reservation_service.find_reservations_for_admin(user.id)

@router.get("/reservations/available-times", response_model=AvailableTimesResponse)
def get_available_times(
    reservation_date: date,
    reservation_service: ReservationService = Depends()
):
    return reservation_service.find_available_reservations(reservation_date)


@router.put("/reservations/{reservation_id}", status_code=status.HTTP_200_OK)
def modify_reservation(
        reservation_id: int,
        request: UpdateReservationRequest,
        user: User = Depends(auth_service.get_current_user),
        reservation_service: ReservationService = Depends()
):
    reservation_service.modify_reservation(user.id, reservation_id, request)
    return {"message": "예약이 수정되었습니다."}


@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_200_OK)
def cancel_reservation(
        reservation_id: int,
        user: User = Depends(auth_service.get_current_user),
        reservation_service: ReservationService = Depends()
):
    reservation_service.cancel_reservation(user.id, reservation_id)
    return {"message": "예약이 취소되었습니다."}


@router.patch("/reservations/{reservation_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_reservation(
        reservation_id: int,
        user: User = Depends(auth_service.get_current_user),
        reservation_service: ReservationService = Depends()
):
    reservation_service.confirm_reservation(user.id, reservation_id)
    return {"message": "예약이 확정되었습니다."}