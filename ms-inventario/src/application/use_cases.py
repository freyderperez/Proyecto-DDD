from uuid import UUID

from domain.entities import Insumo
from domain.repositories import InsumoRepository
from domain.value_objects import CantidadStock, Nombre, Categoria

class RegistrarInsumos:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID, nombre: str, categoria: str, stock_actual: int, stock_min: int, stock_max: int) -> Insumo:
        nombre_vo = Nombre(nombre)
        categoria_vo = Categoria(categoria)
        stock_vo = CantidadStock(stock_actual, stock_min, stock_max)
        insumo = Insumo(id_, nombre_vo, categoria_vo, stock_vo)
        self.repo.save(insumo)
        return insumo

class ConsultarInsumos:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Insumo:
        return self.repo.get_by_id(id_)

class VerificarDisponibilidad:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID, cantidad: int) -> bool:
        insumo = self.repo.get_by_id(id_)
        return insumo.verificar_disponibilidad(cantidad)