from typing import List

from domain.repositories import EmpleadoRepository
from domain.entities import Empleado

class ConsultarEmpleados:
    def __init__(self, repo: EmpleadoRepository):
        self.repo = repo

    def execute(self) -> List[Empleado]:
        return self.repo.get_all()