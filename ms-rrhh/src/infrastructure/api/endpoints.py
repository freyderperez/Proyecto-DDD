from fastapi import APIRouter

router = APIRouter()

@router.get("/empleados")
def get_empleados():
    # Mock for scaffold
    return [{"id": "uuid", "cedula": "123", "estado": "activo"}]

@router.get("/empleados/{id}/estado")
def get_estado(id: str):
    return {"estado": "activo", "activo": True}

@router.get("/health")
def health():
    return {"status": "ok"}