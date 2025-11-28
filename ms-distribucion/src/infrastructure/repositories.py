from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from domain.repositories import EntregaRepository
from domain.entities import Entrega
from domain.value_objects import CantidadSolicitada, EstadoEntrega
from .db.models import EntregaModel

class SQLAlchemyEntregaRepository(EntregaRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, entrega: Entrega) -> None:
        model = EntregaModel(
            id=entrega.id,
            empleado_id=entrega.empleado_id,
            insumo_id=entrega.insumo_id,
            cantidad=int(entrega.cantidad),
            estado=str(entrega.estado)
        )
        self.session.merge(model)
        self.session.commit()

    def get_by_id(self, id_: UUID) -> Entrega:
        model = self.session.query(EntregaModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Entrega not found")
        cantidad = CantidadSolicitada(model.cantidad)
        estado = EstadoEntrega(model.estado)
        return Entrega(model.id, model.empleado_id, model.insumo_id, cantidad, estado)

    def get_all(self) -> List[Entrega]:
        models = self.session.query(EntregaModel).all()
        entregas = []
        for model in models:
            cantidad = CantidadSolicitada(model.cantidad)
            estado = EstadoEntrega(model.estado)
            entregas.append(Entrega(model.id, model.empleado_id, model.insumo_id, cantidad, estado))
        return entregas

    def update(self, entrega: Entrega) -> None:
        model = self.session.query(EntregaModel).filter_by(id=entrega.id).first()
        if not model:
            raise ValueError("Entrega not found")
        model.empleado_id = entrega.empleado_id
        model.insumo_id = entrega.insumo_id
        model.cantidad = int(entrega.cantidad)
        model.estado = str(entrega.estado)
        self.session.commit()

    def delete(self, id_: UUID) -> None:
        model = self.session.query(EntregaModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Entrega not found")
        self.session.delete(model)
        self.session.commit()