from dataclasses import dataclass
from uuid import UUID

@dataclass
class DomainEvent:
    empleado_id: UUID

@dataclass
class EmpleadoCreado(DomainEvent):
    pass

@dataclass
class EmpleadoActualizado(DomainEvent):
    pass

@dataclass
class EmpleadoEliminado(DomainEvent):
    pass