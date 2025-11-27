from fastapi import FastAPI
from infrastructure.api.endpoints import router as api_router

app = FastAPI(title="ms-inventario", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)