from uuid import UUID
from typing import List

from domain.repositories import EntregaRepository
from domain.entities import Entrega
from domain.value_objects import CantidadSolicitada, EstadoEntrega

class RegistrarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, empleado_id: UUID, insumo_id: UUID, cantidad: int) -> Entrega:
        cantidad_vo = CantidadSolicitada(cantidad)
        estado_vo = EstadoEntrega("PENDIENTE")
        entrega = Entrega(empleado_id, insumo_id, cantidad_vo, estado_vo)
        self.repo.save(entrega)
        return entrega

class ListarEntregas:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self) -> List[Entrega]:
        return self.repo.get_all()

class ConsultarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Entrega:
        return self.repo.get_by_id(id_)

class ActualizarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID, empleado_id: UUID = None, insumo_id: UUID = None, cantidad: int = None, estado: str = None) -> Entrega:
        entrega = self.repo.get_by_id(id_)
        if empleado_id is not None:
            entrega.empleado_id = empleado_id
        if insumo_id is not None:
            entrega.insumo_id = insumo_id
        if cantidad is not None:
            entrega.cantidad = CantidadSolicitada(cantidad)
        if estado is not None:
            entrega.estado = EstadoEntrega(estado)
        self.repo.update(entrega)
        return entrega

class EliminarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> None:
        self.repo.delete(id_)

class ConfirmarEntrega:
    def __init__(self, repo: EntregaRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Entrega:
        entrega = self.repo.get_by_id(id_)
        entrega.confirmar()
        self.repo.save(entrega)
        return entrega