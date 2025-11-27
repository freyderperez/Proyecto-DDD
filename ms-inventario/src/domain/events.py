from dataclasses import dataclass
from uuid import UUID

@dataclass
class DomainEvent:
    insumo_id: UUID

@dataclass
class StockAgotado(DomainEvent):
    pass

@dataclass
class StockBajo(DomainEvent):
    pass

@dataclass
class StockExceso(DomainEvent):
    pass

@dataclass
class StockReservado(DomainEvent):
    cantidad: int

@dataclass
class FalloSinStock(DomainEvent):
    cantidad_solicitada: int