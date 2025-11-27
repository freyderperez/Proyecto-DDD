from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmpleadoModel(Base):
    __tablename__ = "empleados"

    id = Column(UUID(as_uuid=True), primary_key=True)
    cedula = Column(String, unique=True, nullable=False)
    estado = Column(String, nullable=False)