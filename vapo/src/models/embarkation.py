from sqlalchemy import Column, Integer, ForeignKey, Date, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base 


class Embarkation(Base):
    __tablename__ = "embarkations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relacionamento com User
    vessel_id = Column(Integer, ForeignKey('vessels.id'), nullable=False)  # Relacionamento com Vessel
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # Relacionamento com Category
    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)  # Relacionamento com Function
    embarkation_location = Column(String, nullable=False)  # Local de embarque
    embarkation_date = Column(Date, nullable=False)  # Data de embarque
    disembarkation_location = Column(String, nullable=False)  # Local de desembarque
    disembarkation_date = Column(Date, nullable=False)  # Data de desembarque
    is_active = Column(Boolean, default=True)  # True = Embarque ativo, False = Embarque concluído

    # Relacionamentos
    user = relationship("User", backref="embarkations")  # Um embarque pertence a um usuário
    vessel = relationship("Vessel", backref="embarkations")  # Um embarque está associado a uma embarcação
    category = relationship("Category", backref="embarkations")  # Um embarque está associado a uma categoria
    function = relationship("Function", backref="embarkations")  # Um embarque está associado a uma função

    def __repr__(self):
        return f"<Embarkation(id={self.id}, user={self.user.name}, vessel={self.vessel.name}, embarkation={self.embarkation_date}, disembarkation={self.disembarkation_date})>"
