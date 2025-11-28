from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from .entities import Insumo

class InsumoRepository(ABC):
    @abstractmethod
    def save(self, insumo: Insumo) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id_: UUID) -> Insumo:
        pass

    @abstractmethod
    def get_all(self) -> List[Insumo]:
        pass

    @abstractmethod
    def update(self, insumo: Insumo) -> None:
        pass

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        pass