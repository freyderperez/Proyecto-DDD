from sqlalchemy.orm import Session

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