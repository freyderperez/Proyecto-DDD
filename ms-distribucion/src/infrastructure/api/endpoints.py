from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from application.use_cases import (
    RegistrarEntrega, ListarEntregas, ConsultarEntrega, ActualizarEntrega, EliminarEntrega, ConfirmarEntrega
)
from application.dto import EntregaCreate, EntregaUpdate, EntregaResponse
from infrastructure.repositories import SQLAlchemyEntregaRepository
from infrastructure.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/distribucion")

@router.post("/entregas", response_model=EntregaResponse)
def create_entrega(request: EntregaCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = RegistrarEntrega(repo)
    try:
        entrega = use_case.execute(UUID(request.empleado_id), UUID(request.insumo_id), request.cantidad)
        return EntregaResponse(
            id=str(entrega.id),
            empleado_id=str(entrega.empleado_id),
            insumo_id=str(entrega.insumo_id),
            cantidad=int(entrega.cantidad),
            estado=str(entrega.estado)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/entregas", response_model=List[EntregaResponse])
def list_entregas(db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = ListarEntregas(repo)
    entregas = use_case.execute()
    return [
        EntregaResponse(
            id=str(e.id),
            empleado_id=str(e.empleado_id),
            insumo_id=str(e.insumo_id),
            cantidad=int(e.cantidad),
            estado=str(e.estado)
        )
        for e in entregas
    ]

@router.get("/entregas/{id}", response_model=EntregaResponse)
def get_entrega(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = ConsultarEntrega(repo)
    try:
        entrega = use_case.execute(UUID(id))
        return EntregaResponse(
            id=str(entrega.id),
            empleado_id=str(entrega.empleado_id),
            insumo_id=str(entrega.insumo_id),
            cantidad=int(entrega.cantidad),
            estado=str(entrega.estado)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/entregas/{id}", response_model=EntregaResponse)
def update_entrega(id: str, request: EntregaUpdate, db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = ActualizarEntrega(repo)
    try:
        entrega = use_case.execute(UUID(id), UUID(request.empleado_id) if request.empleado_id else None, UUID(request.insumo_id) if request.insumo_id else None, request.cantidad, request.estado)
        return EntregaResponse(
            id=str(entrega.id),
            empleado_id=str(entrega.empleado_id),
            insumo_id=str(entrega.insumo_id),
            cantidad=int(entrega.cantidad),
            estado=str(entrega.estado)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/entregas/{id}")
def delete_entrega(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = EliminarEntrega(repo)
    try:
        use_case.execute(UUID(id))
        return {"message": "Entrega deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/entregas/{id}/confirmar", response_model=EntregaResponse)
def confirmar_entrega(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyEntregaRepository(db)
    use_case = ConfirmarEntrega(repo)
    try:
        entrega = use_case.execute(UUID(id))
        return EntregaResponse(
            id=str(entrega.id),
            empleado_id=str(entrega.empleado_id),
            insumo_id=str(entrega.insumo_id),
            cantidad=int(entrega.cantidad),
            estado=str(entrega.estado)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/health")
def health():
    return {"status": "ok"}