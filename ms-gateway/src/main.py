from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway DelegInsumos")

client = httpx.AsyncClient()

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
    response = await client.request(
        method=request.method,
        url=url,
        headers=dict(request.headers),
        content=body,
        params=request.query_params
    )
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=dict(response.headers)
    )

@app.get("/")
def health():
    return {"status": "API Gateway is running"}