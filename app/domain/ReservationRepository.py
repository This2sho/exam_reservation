from typing import List

from sqlalchemy.orm import Session
from app.domain.Reservation import Reservation
from app.domain.ReservationStatus import ReservationStatus
from datetime import date, time


class ReservationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, reservation: Reservation):
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def get_by_id(self, reservation_id: int):
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()

    def delete(self, reservation: Reservation):
        if reservation:
            self.db.delete(reservation)
            self.db.commit()
        return reservation

    def update(self, reservation: Reservation):
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def get_reservations_in_time_range(self, reservation_date: date, start_time: time, end_time: time) -> List[
        Reservation]:
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.date == reservation_date,
                Reservation.status == ReservationStatus.CONFIRMED,
                Reservation.start_time < end_time,
                Reservation.end_time > start_time
            )
            .all()
        )

    def get_by_user_id(self, user_id: int) -> List[Reservation]:
        return self.db.query(Reservation).filter(Reservation.user_id == user_id).all()

    def get_by_date(self, reservation_date: date) -> List[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.date == reservation_date,
                    Reservation.status == ReservationStatus.CONFIRMED
            )
        )

    def get_all(self) -> List[Reservation]:
        return self.db.query(Reservation).all()