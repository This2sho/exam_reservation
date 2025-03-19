from typing import List, Tuple
from app.domain.Reservation import Reservation
from app.domain.User import User
from datetime import date, timedelta, time


class ReservationManagement:
    MIN_DAY = 3
    MAX_PARTICIPANTS = 50_000

    @classmethod
    def is_valid_date(cls, reservation_date: date) -> bool:
        today = date.today()
        return reservation_date >= (today + timedelta(days=cls.MIN_DAY))

    @classmethod
    def is_reservation_possible(cls, existing_reservations: List[Reservation], new_participants: int) -> bool:
        total_reserved = sum(res.num_participants for res in existing_reservations)
        return (total_reserved + new_participants) <= cls.MAX_PARTICIPANTS

    @staticmethod
    def can_confirm_reservation(user: User, reservation: Reservation) -> bool:
        return user.is_admin() and reservation.is_requested()

    @staticmethod
    def can_modify_reservation(user: User, reservation: Reservation) -> bool:
        return user.is_admin() or (reservation.user_id == user.id and reservation.is_requested())

    @staticmethod
    def can_cancel_reservation(user: User, reservation: Reservation) -> bool:
        return user.is_admin() or (reservation.user_id == user.id and reservation.is_requested())

    @classmethod
    def get_available_slots(cls, existing_reservations: List[Reservation]) -> List[
        Tuple[time, time, int]]:
        available_slots = []

        for hour in range(9, 24):
            start_time = time(hour, 0)
            end_time = time(hour + 1, 0)

            reserved_count = sum(
                res.num_participants
                for res in existing_reservations
                if res.start_time >= start_time and res.end_time <= end_time
            )

            available_spots = max(0, cls.MAX_PARTICIPANTS - reserved_count)
            available_slots.append((start_time, end_time, available_spots))
        return available_slots
