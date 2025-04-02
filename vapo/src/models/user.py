from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)  # Relacionamento com Function
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # Relacionamento com Category
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relacionamentos
    function = relationship("Function", backref="users")  # Um usuário tem uma função
    category = relationship("Category", backref="users")  # Um usuário pertence a uma categoria

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, function={self.function.name}, category={self.category.name})>"
