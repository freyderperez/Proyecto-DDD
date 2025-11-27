from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Entrega

class EntregaRepository(ABC):
    @abstractmethod
    def save(self, entrega: Entrega) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id_: UUID) -> Entrega:
        pass