
from sqlalchemy import Column, BigInteger, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from app.domain.UserRole import UserRole
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    email = Column(String, nullable=False, unique=True)

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

