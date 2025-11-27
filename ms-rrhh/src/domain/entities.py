from uuid import UUID

from .value_objects import Cedula, EstadoEmpleado

class Empleado:
    def __init__(self, id_: UUID, cedula: Cedula, estado: EstadoEmpleado):
        self.id = id_
        self.cedula = cedula
        self.estado = estado

    def es_activo(self) -> bool:
        return self.estado == "activo"