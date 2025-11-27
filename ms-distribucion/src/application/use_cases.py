from uuid import UUID

from domain.repositories import EntregaRepository
from domain.entities import Entrega
from domain.value_objects import CantidadSolicitada, EstadoEntrega

class RegistrarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID, empleado_id: UUID, insumo_id: UUID, cantidad: int) -> Entrega:
        cantidad_vo = CantidadSolicitada(cantidad)
        estado_vo = EstadoEntrega("PENDIENTE")
        entrega = Entrega(id_, empleado_id, insumo_id, cantidad_vo, estado_vo)
        self.repo.save(entrega)
        return entrega

class ConfirmarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Entrega:
        entrega = self.repo.get_by_id(id_)
        entrega.confirmar()
        self.repo.save(entrega)
        return entrega