from sqlalchemy import Column, Integer, String, Text
from .base import Base 


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Nome da categoria
    abbreviation = Column(String(10), unique=True, nullable=False)  # Abreviação da categoria
    description = Column(Text, nullable=True)  # Descrição da categoria (opcional)

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, abbreviation={self.abbreviation}, description={self.description})>"
