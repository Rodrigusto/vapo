from sqlalchemy import Column, Integer, String, Text
from .base import Base 


class Certificate(Base):
    """
    Certificate model.
    id=pk, name=str, validate=str, description=str, image=str
    """
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Limita o tamanho do nome
    validate = Column(String(10), nullable=False)  # Formato de data fixo
    description = Column(Text, nullable=True)
    image = Column(String(200))  # Limita o tamanho do caminho da imagem
    
    def __repr__(self):
        return f"<Certificate(id={self.id}, name={self.name}, validate={self.validate}, description={self.description}, image={self.image})>"
