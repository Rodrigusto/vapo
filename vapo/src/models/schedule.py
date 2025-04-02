from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base 


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relacionamento com User
    start_date = Column(Date, nullable=False)  # Data de início da escala
    days_on = Column(Integer, nullable=False)  # Dias embarcados
    days_off = Column(Integer, nullable=False)  # Dias em terra

    # Relacionamentos
    user = relationship("User", backref="schedules")  # Uma escala pertence a um usuário

    def __repr__(self):
        return f"<Schedule(id={self.id}, user={self.user.name}, start_date={self.start_date}, days_on={self.days_on}, days_off={self.days_off})>"
