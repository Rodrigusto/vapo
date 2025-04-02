# models/vessel.py
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Importe Base do arquivo centralizado

class Vessel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    imo_number = Column(String, unique=True, nullable=False)
    gross_tonnage = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    vessel_type_id = Column(Integer, ForeignKey('vessel_types.id'), nullable=False)

    # Relacionamentos
    vessel_type = relationship("VesselType", backref="vessels")

    def __repr__(self):
        return f"<Vessel(id={self.id}, name={self.name}, description={self.description}, imo_number={self.imo_number}, gross_tonnage={self.gross_tonnage}, power={self.power}, type={self.vessel_type.name})>"