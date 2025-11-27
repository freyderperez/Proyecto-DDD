from uuid import UUID

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
            nombre=insumo.nombre.value,
            categoria=insumo.categoria.value,
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
        return Insumo(model.id, nombre, categoria, stock)