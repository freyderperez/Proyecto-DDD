from pydantic import BaseModel
from typing import Optional

class EmpleadoCreate(BaseModel):
    cedula: str
    estado: str
    nombre_completo: str
    cargo: str
    departamento: str
    email: str
    telefono: str

class EmpleadoUpdate(BaseModel):
    cedula: Optional[str] = None
    estado: Optional[str] = None
    nombre_completo: Optional[str] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

class EmpleadoResponse(BaseModel):
    id: str
    cedula: str
    estado: str
    nombre_completo: str
    cargo: str
    departamento: str
    email: str
    telefono: str

class EstadoResponse(BaseModel):
    estado: str
    activo: bool