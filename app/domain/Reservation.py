from sqlalchemy import Column, Integer, BigInteger, Date, Time, Enum, ForeignKey
from app.domain.ReservationStatus import ReservationStatus
from app.domain.User import User
from app.database.database import Base

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    num_participants = Column(Integer, nullable=False)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.REQUESTED)

    def is_requested(self) -> bool:
        return self.status == ReservationStatus.REQUESTED
