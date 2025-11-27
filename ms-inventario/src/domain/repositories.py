from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Insumo

class InsumoRepository(ABC):
    @abstractmethod
    def save(self, insumo: Insumo) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id_: UUID) -> Insumo:
        pass