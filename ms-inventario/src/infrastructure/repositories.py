from uuid import UUID
from typing import List

from sqlalchemy.orm import Session

from domain.repositories import InsumoRepository
from domain.entities import Insumo
from domain.value_objects import CantidadStock, Nombre, Categoria
from .db.models import InsumoModel

class SQLAlchemyInsumoRepository(InsumoRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, insumo: Insumo) -> None:
        model = InsumoModel(
            id=insumo.id,
            nombre=insumo.nombre,
            categoria=insumo.categoria,
            stock_actual=insumo.stock.actual,
            stock_min=insumo.stock.min,
            stock_max=insumo.stock.max
        )
        self.session.merge(model)
        self.session.commit()

    def get_by_id(self, id_: UUID) -> Insumo:
        model = self.session.query(InsumoModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Insumo not found")
        nombre = Nombre(model.nombre)
        categoria = Categoria(model.categoria)
        stock = CantidadStock(model.stock_actual, model.stock_min, model.stock_max)
        return Insumo(nombre, categoria, stock, model.id)

    def get_all(self) -> List[Insumo]:
        models = self.session.query(InsumoModel).all()
        insumos = []
        for model in models:
            nombre = Nombre(model.nombre)
            categoria = Categoria(model.categoria)
            stock = CantidadStock(model.stock_actual, model.stock_min, model.stock_max)
            insumos.append(Insumo(nombre, categoria, stock, model.id))
        return insumos

    def update(self, insumo: Insumo) -> None:
        model = self.session.query(InsumoModel).filter_by(id=insumo.id).first()
        if not model:
            raise ValueError("Insumo not found")
        model.nombre = insumo.nombre
        model.categoria = insumo.categoria
        model.stock_actual = insumo.stock.actual
        model.stock_min = insumo.stock.min
        model.stock_max = insumo.stock.max
        self.session.commit()

    def delete(self, id_: UUID) -> None:
        model = self.session.query(InsumoModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Insumo not found")
        self.session.delete(model)
        self.session.commit()