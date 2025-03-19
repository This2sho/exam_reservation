from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date, time

from app.api.dto.request.CreateReservationRequest import CreateReservationRequest
from app.api.dto.request.UpdateReservationRequest import UpdateReservationRequest
from app.api.dto.response.AdminReservationDetailResponse import AdminReservationDetailResponse
from app.api.dto.response.AdminReservationsResponse import AdminReservationsResponse
from app.api.dto.response.AvailableSlotResponse import AvailableSlotResponse
from app.api.dto.response.AvailableTimesResponse import AvailableTimesResponse
from app.api.dto.response.CreateReservationResponse import CreateReservationResponse
from app.api.dto.response.ReservationDetailResponse import ReservationDetailResponse
from app.api.dto.response.ReservationsResponse import ReservationsResponse
from app.domain.Reservation import Reservation
from app.domain.ReservationManagement import ReservationManagement
from app.domain.ReservationRepository import ReservationRepository
from app.domain.ReservationStatus import ReservationStatus
from app.domain.UserRepository import UserRepository


class ReservationService:

    def __init__(self, db: Session):
        self.reservation_repository = ReservationRepository(db)
        self.user_repository = UserRepository(db)

    def create_reservation(self, request: CreateReservationRequest, user_id: int) -> CreateReservationResponse:
        self.validate_reservation(request.reservation_date, request.start_time, request.end_time,
                                  request.num_participants)

        reservation = Reservation(date=request.reservation_date, start_time=request.start_time,
                                  end_time=request.end_time, num_participants=request.num_participants,
                                  user_id=user_id, status=ReservationStatus.REQUESTED)
        create = self.reservation_repository.create(reservation)
        return CreateReservationResponse(reservation_id=create.id)

    def validate_reservation(self, reservation_date: date, start_time: time, end_time: time, num_participants: int):
        if not ReservationManagement.is_valid_date(reservation_date):
            raise ValueError(f"{reservation_date}은 예약이 불가능합니다. 최소 3일 전에 신청 가능합니다.")
        existing_reservations = self.reservation_repository.get_reservations_in_time_range(reservation_date,
                                                                                           start_time,
                                                                                           end_time)
        if not ReservationManagement.is_reservation_possible(existing_reservations, num_participants):
            raise ValueError("해당 시간대 예약이 가득 찼습니다.")

    def find_reservations(self, user_id: int) -> ReservationsResponse:
        reservations = self.reservation_repository.get_by_user_id(user_id)
        response_data = [
            ReservationDetailResponse(
                reservation_id=res.id,
                date=res.date,
                start_time=res.start_time,
                end_time=res.end_time,
                num_participants=res.num_participants,
                status=res.status
            )
            for res in reservations
        ]
        return ReservationsResponse(reservations=response_data)

    def find_available_reservations(self, reservation_date: date) -> AvailableTimesResponse:
        existing_reservations = self.reservation_repository.get_by_date(reservation_date)
        available_slots = ReservationManagement.get_available_slots(existing_reservations)

        return AvailableTimesResponse(
            date=reservation_date,
            available_slots=[
                AvailableSlotResponse(start_time=start, end_time=end, available_spots=spots)
                for start, end, spots in available_slots
            ]
        )

    def find_reservations_for_admin(self, user_id: int) -> AdminReservationsResponse:
        user = self.user_repository.get_by_id(user_id)

        if not user.is_admin():
            raise HTTPException(status_code=403, detail="권한이 없습니다.")
        reservations = self.reservation_repository.get_all()
        response_data = [
            AdminReservationDetailResponse(
                reservation_id=res.id,
                date=res.date,
                start_time=res.start_time,
                end_time=res.end_time,
                num_participants=res.num_participants,
                status=res.status,
                user_id=res.user_id
            )
            for res in reservations
        ]
        return AdminReservationsResponse(reservations=response_data)

    def confirm_reservation(self, user_id: int, reservation_id: int):
        user = self.user_repository.get_by_id(user_id)
        reservation = self.reservation_repository.get_by_id(reservation_id)

        if not ReservationManagement.can_confirm_reservation(user, reservation):
            raise ValueError("예약을 확정할 수 없습니다.")
        reservation.status = ReservationStatus.CONFIRMED
        self.reservation_repository.update(reservation)

    def modify_reservation(self, user_id: int, reservation_id: int, request: UpdateReservationRequest):
        self.validate_reservation(request.date, request.start_time, request.end_time, request.num_participants)
        user = self.user_repository.get_by_id(user_id)
        reservation = self.reservation_repository.get_by_id(reservation_id)
        if not ReservationManagement.can_modify_reservation(user, reservation):
            raise ValueError("예약을 변경할 수 없습니다.")

        reservation.date = request.date
        reservation.start_time = request.start_time
        reservation.end_time = request.end_time
        reservation.num_participants = request.num_participants
        self.reservation_repository.update(reservation)

    def cancel_reservation(self, user_id: int, reservation_id: int):
        user = self.user_repository.get_by_id(user_id)
        reservation = self.reservation_repository.get_by_id(reservation_id)

        if not ReservationManagement.can_cancel_reservation(user, reservation):
            raise ValueError("예약을 취소할 수 없습니다.")
        reservation.status = ReservationStatus.CANCELLED
        self.reservation_repository.update(reservation)
