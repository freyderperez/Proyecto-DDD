from dataclasses import dataclass
from uuid import UUID

@dataclass
class DomainEvent:
    entrega_id: UUID

@dataclass
class EntregaRegistrada(DomainEvent):
    pass

@dataclass
class EntregaConfirmada(DomainEvent):
    pass