from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from .entities import Empleado

class EmpleadoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id_: UUID) -> Empleado:
        pass

    @abstractmethod
    def get_all(self) -> List[Empleado]:
        pass