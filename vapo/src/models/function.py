from sqlalchemy import Column, Integer, String, Text
from .base import Base 


class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Nome da função
    abbreviation = Column(String(10), unique=True, nullable=False)  # Abreviação da função
    description = Column(Text, nullable=True)  # Descrição da função (opcional)

    def __repr__(self):
        return f"<Function(id={self.id}, name={self.name}, abbreviation={self.abbreviation}, description={self.description})>"
