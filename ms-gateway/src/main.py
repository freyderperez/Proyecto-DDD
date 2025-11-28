from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway DelegInsumos")

# 🔥 HEALTHCHECK debe ir ANTES del proxy para no ser sobrescrito
@app.get("/")
def health():
    return {"status": "API Gateway is running"}

@app.get("/inventario/insumos")
async def health_inventario():
    try:
        response = await client.get("http://ms-inventario:8001/inventario/insumos")
        return Response(status_code=response.status_code, content=response.content)
    except:
        return {"error": "Inventario service unavailable"}

@app.get("/rrhh/empleados")
async def health_rrhh():
    try:
        response = await client.get("http://ms-rrhh:8003/rrhh/empleados")
        return Response(status_code=response.status_code, content=response.content)
    except:
        return {"error": "RRHH service unavailable"}

@app.get("/distribucion/entregas")
async def health_distribucion():
    try:
        response = await client.get("http://ms-distribucion:8002/distribucion/entregas")
        return Response(status_code=response.status_code, content=response.content)
    except:
        return {"error": "Distribucion service unavailable"}

client = httpx.AsyncClient()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    # Rutas por prefijo
    if path.startswith("inventario/"):
        url = f"http://ms-inventario:8001/{path}"
    elif path.startswith("distribucion/"):
        url = f"http://ms-distribucion:8002/{path}"
    elif path.startswith("rrhh/"):
        url = f"http://ms-rrhh:8003/{path}"
    else:
        return Response(status_code=404, content="Not found")

    try:
        # Forward request
        body = await request.body()
        response = await client.request(
            method=request.method,
            url=url,
            headers={k:v for k,v in request.headers.items() if k != "host"},
            content=body,
            params=request.query_params
        )

        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=dict(response.headers)
        )
    except httpx.RequestError as e:
        return Response(status_code=503, content=f"Service unavailable: {str(e)}")
    except Exception as e:
        return Response(status_code=500, content=f"Internal server error: {str(e)}")
