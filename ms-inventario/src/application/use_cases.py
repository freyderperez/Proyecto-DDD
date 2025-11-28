from uuid import UUID
from typing import List

from domain.entities import Insumo
from domain.repositories import InsumoRepository
from domain.value_objects import CantidadStock, Nombre, Categoria

class RegistrarInsumos:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, nombre: str, categoria: str, stock_actual: int, stock_min: int, stock_max: int) -> Insumo:
        nombre_vo = Nombre(nombre)
        categoria_vo = Categoria(categoria)
        stock_vo = CantidadStock(stock_actual, stock_min, stock_max)
        insumo = Insumo(nombre_vo, categoria_vo, stock_vo)
        self.repo.save(insumo)
        return insumo

class ConsultarInsumos:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> Insumo:
        return self.repo.get_by_id(id_)

class ListarInsumos:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self) -> List[Insumo]:
        return self.repo.get_all()

class ActualizarInsumo:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID, nombre: str = None, categoria: str = None, stock_actual: int = None, stock_min: int = None, stock_max: int = None) -> Insumo:
        insumo = self.repo.get_by_id(id_)
        if nombre is not None:
            insumo.nombre = Nombre(nombre)
        if categoria is not None:
            insumo.categoria = Categoria(categoria)
        if stock_actual is not None and stock_min is not None and stock_max is not None:
            insumo.stock = CantidadStock(stock_actual, stock_min, stock_max)
        self.repo.update(insumo)
        return insumo

class EliminarInsumo:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID) -> None:
        self.repo.delete(id_)

class VerificarDisponibilidad:
    def __init__(self, repo: InsumoRepository):
        self.repo = repo

    def execute(self, id_: UUID, cantidad: int) -> bool:
        insumo = self.repo.get_by_id(id_)
        return insumo.verificar_disponibilidad(cantidad)