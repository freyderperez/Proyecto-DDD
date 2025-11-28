from uuid import uuid4, UUID

from .value_objects import CantidadSolicitada, EstadoEntrega

class Entrega:
    def __init__(self, empleado_id: UUID, insumo_id: UUID, cantidad: CantidadSolicitada, estado: EstadoEntrega):
        self.id = uuid4()
        self.empleado_id = empleado_id
        self.insumo_id = insumo_id
        self.cantidad = cantidad
        self.estado = estado

    def confirmar(self):
        self.estado = EstadoEntrega("CONFIRMADA")