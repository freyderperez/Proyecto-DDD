from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from .session import Base

class EmpleadoModel(Base):
    __tablename__ = "empleados"

    id = Column(UUID(as_uuid=True), primary_key=True)
    cedula = Column(String, unique=True, nullable=False)
    estado = Column(String, nullable=False)