from fastapi import FastAPI, Request, Response
import httpx
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = httpx.AsyncClient()
    yield
    await client.aclose()

app = FastAPI(title="API Gateway DelegInsumos", lifespan=lifespan)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    if path.startswith("inventario/"):
        url = f"http://ms-inventario:8001/{path}"
    elif path.startswith("distribucion/"):
        url = f"http://ms-distribucion:8002/{path}"
    elif path.startswith("rrhh/"):
        url = f"http://ms-rrhh:8003/{path}"
    else:
        return Response(status_code=404, content="Not found")

    body = await request.body()
    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=body,
            params=request.query_params
        )
    except httpx.RequestError:
        return Response(status_code=502, content="Bad Gateway")
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=dict(response.headers)
    )

@app.get("/")
def health():
    return {"status": "API Gateway is running"}