from pydantic import BaseModel
from typing import Optional

class EntregaCreate(BaseModel):
    empleado_id: str
    insumo_id: str
    cantidad: int

class EntregaUpdate(BaseModel):
    empleado_id: Optional[str] = None
    insumo_id: Optional[str] = None
    cantidad: Optional[int] = None
    estado: Optional[str] = None

class EntregaResponse(BaseModel):
    id: str
    empleado_id: str
    insumo_id: str
    cantidad: int
    estado: str