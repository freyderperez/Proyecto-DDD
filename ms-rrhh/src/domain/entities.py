from uuid import uuid4

from .value_objects import Cedula, EstadoEmpleado

class Empleado:
    def __init__(self, cedula: Cedula, estado: EstadoEmpleado):
        self.id = uuid4()
        self.cedula = cedula
        self.estado = estado

    def es_activo(self) -> bool:
        return self.estado == "activo"