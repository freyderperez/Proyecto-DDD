from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from application.use_cases import (
    RegistrarInsumos, ConsultarInsumos, ListarInsumos, ActualizarInsumo, EliminarInsumo, VerificarDisponibilidad
)
from application.dto import InsumoCreate, InsumoUpdate, InsumoResponse, StockDTO, DisponibilidadResponse
from infrastructure.repositories import SQLAlchemyInsumoRepository
from infrastructure.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/inventario")

@router.post("/insumos", response_model=InsumoResponse)
def create_insumo(request: InsumoCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = RegistrarInsumos(repo)
    try:
        insumo = use_case.execute(request.nombre, request.categoria, request.stock_actual, request.stock_min, request.stock_max)
        return InsumoResponse(
            id=str(insumo.id),
            nombre=insumo.nombre,
            categoria=insumo.categoria,
            stock=StockDTO(actual=insumo.stock.actual, min=insumo.stock.min, max=insumo.stock.max)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/insumos", response_model=List[InsumoResponse])
def list_insumos(db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = ListarInsumos(repo)
    insumos = use_case.execute()
    return [
        InsumoResponse(
            id=str(i.id),
            nombre=i.nombre,
            categoria=i.categoria,
            stock=StockDTO(actual=i.stock.actual, min=i.stock.min, max=i.stock.max)
        )
        for i in insumos
    ]

@router.get("/insumos/{id}", response_model=InsumoResponse)
def get_insumo(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = ConsultarInsumos(repo)
    try:
        insumo = use_case.execute(UUID(id))
        return InsumoResponse(
            id=str(insumo.id),
            nombre=insumo.nombre,
            categoria=insumo.categoria,
            stock=StockDTO(actual=insumo.stock.actual, min=insumo.stock.min, max=insumo.stock.max)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/insumos/{id}", response_model=InsumoResponse)
def update_insumo(id: str, request: InsumoUpdate, db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = ActualizarInsumo(repo)
    try:
        insumo = use_case.execute(UUID(id), request.nombre, request.categoria, request.stock_actual, request.stock_min, request.stock_max)
        return InsumoResponse(
            id=str(insumo.id),
            nombre=insumo.nombre,
            categoria=insumo.categoria,
            stock=StockDTO(actual=insumo.stock.actual, min=insumo.stock.min, max=insumo.stock.max)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/insumos/{id}")
def delete_insumo(id: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = EliminarInsumo(repo)
    try:
        use_case.execute(UUID(id))
        return {"message": "Insumo deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/insumos/{id}/disponibilidad", response_model=DisponibilidadResponse)
def check_disponibilidad(id: str, cantidad: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyInsumoRepository(db)
    use_case = VerificarDisponibilidad(repo)
    try:
        disponible = use_case.execute(UUID(id), cantidad)
        return DisponibilidadResponse(disponible=disponible)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/health")
def health():
    return {"status": "ok"}