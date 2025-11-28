from typing import List
from uuid import UUID

from domain.repositories import EmpleadoRepository
from domain.entities import Empleado
from domain.value_objects import Cedula, EstadoEmpleado

class RegistrarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, cedula: str, estado: str) -> Empleado:
        cedula_vo = Cedula(cedula)
        estado_vo = EstadoEmpleado(estado)
        empleado = Empleado(cedula_vo, estado_vo)
        self.repo.save(empleado)
        return empleado

class ConsultarEmpleados:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self) -> List[Empleado]:
        return self.repo.get_all()

class ConsultarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Empleado:
        return self.repo.get_by_id(id_)

class ActualizarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, id_: UUID, cedula: str = None, estado: str = None) -> Empleado:
        empleado = self.repo.get_by_id(id_)
        if cedula is not None:
            empleado.cedula = Cedula(cedula)
        if estado is not None:
            empleado.estado = EstadoEmpleado(estado)
        self.repo.update(empleado)
        return empleado

class EliminarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> None:
        self.repo.delete(id_)