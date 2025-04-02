from sqlalchemy import Column, Integer, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from .base import Base 



class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relacionamento com User
    vessel_id = Column(Integer, ForeignKey('vessels.id'), nullable=False)  # Relacionamento com Vessel
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # Relacionamento com Category
    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)  # Relacionamento com Function
    total_days_embarked = Column(Float, nullable=False)  # Total de dias embarcados
    valid_certificates = Column(Integer, nullable=False)  # Número de certificados válidos
    expiring_certificates = Column(Integer, nullable=False)  # Número de certificados a vencer
    expired_certificates = Column(Integer, nullable=False)  # Número de certificados vencidos
    generated_at = Column(Date, nullable=False)  # Data de geração do relatório

    # Relacionamentos
    user = relationship("User", backref="reports")  # Um relatório pertence a um usuário
    vessel = relationship("Vessel", backref="reports")  # Um relatório está associado a uma embarcação
    category = relationship("Category", backref="reports")  # Um relatório está associado a uma categoria
    function = relationship("Function", backref="reports")  # Um relatório está associado a uma função

    def __repr__(self):
        return f"<Report(id={self.id}, user={self.user.name}, vessel={self.vessel.name}, total_days={self.total_days_embarked}, valid_certs={self.valid_certificates}, expiring_certs={self.expiring_certificates}, expired_certs={self.expired_certificates})>"
