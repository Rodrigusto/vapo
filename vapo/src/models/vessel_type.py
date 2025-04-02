# models/vessel_type.py
from sqlalchemy import Column, Integer, String, Text
from .base import Base  # Importe Base do arquivo centralizado

class VesselType(Base):
    __tablename__ = "vessel_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    abbreviation = Column(String(10), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<VesselType(id={self.id}, name={self.name}, abbreviation={self.abbreviation}, description={self.description})>"