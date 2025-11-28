from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from application.use_cases import (
    RegistrarEmpleado, ConsultarEmpleados, ConsultarEmpleado, ActualizarEmpleado, EliminarEmpleado
)
from application.dto import EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse, EstadoResponse
from infrastructure.repositories import SQLAlchemyEmpleadoRepository
from infrastructure.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/rrhh")

@router.post("/empleados", response_model=EmpleadoResponse)
def create_empleado(request: EmpleadoCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = RegistrarEmpleado(repo)
    try:
        empleado = use_case.execute(request.cedula, request.estado)
        return EmpleadoResponse(
            id=str(empleado.id),
            cedula=empleado.cedula,
            estado=empleado.estado
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empleados", response_model=List[EmpleadoResponse])
def list_empleados(db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = ConsultarEmpleados(repo)
    empleados = use_case.execute()
    return [
        EmpleadoResponse(
            id=str(e.id),
            cedula=e.cedula,
            estado=e.estado
        )
        for e in empleados
    ]

@router.get("/empleados/{id}", response_model=EmpleadoResponse)
def get_empleado(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = ConsultarEmpleado(repo)
    try:
        empleado = use_case.execute(UUID(id))
        return EmpleadoResponse(
            id=str(empleado.id),
            cedula=empleado.cedula,
            estado=empleado.estado
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/empleados/{id}", response_model=EmpleadoResponse)
def update_empleado(id: str, request: EmpleadoUpdate, db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = ActualizarEmpleado(repo)
    try:
        empleado = use_case.execute(UUID(id), request.cedula, request.estado)
        return EmpleadoResponse(
            id=str(empleado.id),
            cedula=empleado.cedula,
            estado=empleado.estado
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/empleados/{id}")
def delete_empleado(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = EliminarEmpleado(repo)
    try:
        use_case.execute(UUID(id))
        return {"message": "Empleado deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/empleados/{id}/estado", response_model=EstadoResponse)
def get_estado(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEmpleadoRepository(db)
    use_case = ConsultarEmpleado(repo)
    try:
        empleado = use_case.execute(UUID(id))
        return EstadoResponse(estado=empleado.estado, activo=empleado.es_activo())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/health")
def health():
    return {"status": "ok"}