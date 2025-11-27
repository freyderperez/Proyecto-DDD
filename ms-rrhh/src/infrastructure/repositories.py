from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from domain.repositories import EmpleadoRepository
from domain.entities import Empleado
from domain.value_objects import Cedula, EstadoEmpleado
from .db.models import EmpleadoModel

class SQLAlchemyEmpleadoRepository(EmpleadoRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id_: UUID) -> Empleado:
        model = self.session.query(EmpleadoModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Empleado not found")
        cedula = Cedula(model.cedula)
        estado = EstadoEmpleado(model.estado)
        return Empleado(model.id, cedula, estado)

    def get_all(self) -> List[Empleado]:
        models = self.session.query(EmpleadoModel).all()
        empleados = []
        for model in models:
            cedula = Cedula(model.cedula)
            estado = EstadoEmpleado(model.estado)
            empleados.append(Empleado(model.id, cedula, estado))
        return empleados