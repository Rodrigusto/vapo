# database/__init__.py
from .connection import engine, session

# Exportar para uso em outros módulos
__all__ = ["engine", "session"]
