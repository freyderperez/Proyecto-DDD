from pydantic import BaseModel
from typing import Optional

class StockDTO(BaseModel):
    actual: int
    min: int
    max: int

class InsumoCreate(BaseModel):
    nombre: str
    categoria: str
    stock_actual: int
    stock_min: int
    stock_max: int

class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    stock_actual: Optional[int] = None
    stock_min: Optional[int] = None
    stock_max: Optional[int] = None

class InsumoResponse(BaseModel):
    id: str
    nombre: str
    categoria: str
    stock: StockDTO

class DisponibilidadResponse(BaseModel):
    disponible: bool