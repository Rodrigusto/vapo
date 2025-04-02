from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Importe Base do módulo models

# Configuração do banco de dados
DATABASE_URL = "sqlite:///vapo.db"  # Altere para o seu banco de dados

# Cria a engine e a sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sessão global (usada diretamente no código)
session = SessionLocal()

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(engine)