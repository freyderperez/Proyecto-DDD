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

    def save(self, empleado: Empleado) -> None:
        model = EmpleadoModel(
            id=empleado.id,
            cedula=empleado.cedula,
            estado=empleado.estado,
            nombre_completo=empleado.nombre_completo,
            cargo=empleado.cargo,
            departamento=empleado.departamento,
            email=empleado.email,
            telefono=empleado.telefono
        )
        self.session.merge(model)
        self.session.commit()

    def get_by_id(self, id_: UUID) -> Empleado:
        model = self.session.query(EmpleadoModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Empleado not found")
        cedula = Cedula(model.cedula)
        estado = EstadoEmpleado(model.estado)
        return Empleado(cedula, estado, model.nombre_completo, model.cargo, model.departamento, model.email, model.telefono, model.id)

    def get_all(self) -> List[Empleado]:
        models = self.session.query(EmpleadoModel).all()
        empleados = []
        for model in models:
            cedula = Cedula(model.cedula)
            estado = EstadoEmpleado(model.estado)
            empleados.append(Empleado(cedula, estado, model.nombre_completo, model.cargo, model.departamento, model.email, model.telefono, model.id))
        return empleados

    def update(self, empleado: Empleado) -> None:
        model = self.session.query(EmpleadoModel).filter_by(id=empleado.id).first()
        if not model:
            raise ValueError("Empleado not found")
        model.cedula = empleado.cedula
        model.estado = empleado.estado
        model.nombre_completo = empleado.nombre_completo
        model.cargo = empleado.cargo
        model.departamento = empleado.departamento
        model.email = empleado.email
        model.telefono = empleado.telefono
        self.session.commit()

    def delete(self, id_: UUID) -> None:
        model = self.session.query(EmpleadoModel).filter_by(id=id_).first()
        if not model:
            raise ValueError("Empleado not found")
        self.session.delete(model)
        self.session.commit()