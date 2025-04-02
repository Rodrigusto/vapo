# models/__init__.py

# 1. Exporte a classe Base primeiro
from .base import Base

# 2. Exporte as models sem dependências
from .category import Category
from .function import Function

# 3. Exporte as models que dependem de Category e Function
from .user import User

# 4. Exporte as models que dependem de VesselType
from .vessel_type import VesselType
from .vessel import Vessel

# 5. Exporte as models que dependem de User
from .schedule import Schedule
from .certificate import Certificate

# 6. Exporte as models que dependem de User, Vessel, Category e Function
from .embarkation import Embarkation
from .report import Report

# Export all models
__all__ = [
    "Base",
    "Category",
    "Function",
    "User",
    "VesselType",
    "Vessel",
    "Schedule",
    "Embarkation",
    "Certificate",
    "Report"
]