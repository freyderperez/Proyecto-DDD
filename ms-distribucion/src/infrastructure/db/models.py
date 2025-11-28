from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from .session import Base

class EntregaModel(Base):
    __tablename__ = "entregas"

    id = Column(UUID(as_uuid=True), primary_key=True)
    empleado_id = Column(UUID(as_uuid=True), nullable=False)
    insumo_id = Column(UUID(as_uuid=True), nullable=False)
    cantidad = Column(Integer, nullable=False)
    estado = Column(String, nullable=False)