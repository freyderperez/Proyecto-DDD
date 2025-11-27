from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InsumoModel(Base):
    __tablename__ = "insumos"

    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    stock_actual = Column(Integer, nullable=False)
    stock_min = Column(Integer, nullable=False)
    stock_max = Column(Integer, nullable=False)