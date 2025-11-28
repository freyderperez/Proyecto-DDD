from typing import List
from uuid import UUID

from domain.repositories import EmpleadoRepository
from domain.entities import Empleado
from domain.value_objects import Cedula, EstadoEmpleado

class RegistrarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, cedula: str, estado: str, nombre_completo: str, cargo: str, departamento: str, email: str, telefono: str) -> Empleado:
        cedula_vo = Cedula(cedula)
        estado_vo = EstadoEmpleado(estado)
        empleado = Empleado(cedula_vo, estado_vo, nombre_completo, cargo, departamento, email, telefono)
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

    def execute(self, id_: UUID, cedula: str = None, estado: str = None, nombre_completo: str = None, cargo: str = None, departamento: str = None, email: str = None, telefono: str = None) -> Empleado:
        empleado = self.repo.get_by_id(id_)
        if cedula is not None:
            empleado.cedula = Cedula(cedula)
        if estado is not None:
            empleado.estado = EstadoEmpleado(estado)
        if nombre_completo is not None:
            empleado.nombre_completo = nombre_completo
        if cargo is not None:
            empleado.cargo = cargo
        if departamento is not None:
            empleado.departamento = departamento
        if email is not None:
            empleado.email = email
        if telefono is not None:
            empleado.telefono = telefono
        self.repo.update(empleado)
        return empleado

class EliminarEmpleado:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> None:
        self.repo.delete(id_)