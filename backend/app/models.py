from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class CarVelocity(Base):
    __tablename__ = 'car_velocities'
    id = Column(Integer,primary_key=True,  autoincrement=True, nullable=False)
    velocity = Column(Integer, nullable=False)
    citypoint= Column(Integer, nullable=False)
    passed_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
