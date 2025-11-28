import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from infrastructure.api.endpoints import router as api_router

app = FastAPI(title="ms-distribucion", version="1.0.0")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)