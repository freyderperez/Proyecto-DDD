from pydantic import BaseModel
from typing import Optional

class EmpleadoCreate(BaseModel):
    cedula: str
    estado: str

class EmpleadoUpdate(BaseModel):
    cedula: Optional[str] = None
    estado: Optional[str] = None

class EmpleadoResponse(BaseModel):
    id: str
    cedula: str
    estado: str

class EstadoResponse(BaseModel):
    estado: str
    activo: bool