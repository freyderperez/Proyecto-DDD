from uuid import uuid4

from .value_objects import Cedula, EstadoEmpleado

class Empleado:
    def __init__(self, cedula: Cedula, estado: EstadoEmpleado, nombre_completo: str, cargo: str, departamento: str, email: str, telefono: str, id=None):
        self.id = id if id is not None else uuid4()
        self.cedula = cedula
        self.estado = estado
        self.nombre_completo = nombre_completo
        self.cargo = cargo
        self.departamento = departamento
        self.email = email
        self.telefono = telefono

    def es_activo(self) -> bool:
        return self.estado == "activo"