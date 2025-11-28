from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

from .entities import Entrega

class EntregaRepository(ABC):
    @abstractmethod
    def save(self, entrega: Entrega) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id_: UUID) -> Entrega:
        pass

    @abstractmethod
    def get_all(self) -> List[Entrega]:
        pass

    @abstractmethod
    def update(self, entrega: Entrega) -> None:
        pass

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        pass