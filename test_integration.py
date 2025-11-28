import asyncio
import httpx
import uuid

async def test_integration():
    async with httpx.AsyncClient() as client:
        insumo_id = str(uuid.uuid4())
        empleado_id = str(uuid.uuid4())
        entrega_id = str(uuid.uuid4())

        # Health check gateway
        response = await client.get("http://localhost:8000/")
        assert response.status_code == 200

        # Create empleado
        response = await client.post("http://localhost:8000/rrhh/empleados", json={
            "cedula": "123456789",
            "estado": "activo"
        })
        assert response.status_code == 200

        # Create insumo
        response = await client.post("http://localhost:8000/inventario/insumos", json={
            "nombre": "Test Insumo",
            "categoria": "Test",
            "stock_actual": 10,
            "stock_min": 5,
            "stock_max": 20
        })
        assert response.status_code == 200

        # Create entrega
        response = await client.post("http://localhost:8000/distribucion/entregas", json={
            "empleado_id": empleado_id,
            "insumo_id": insumo_id,
            "cantidad": 5
        })
        assert response.status_code == 200

        # Confirm entrega
        response = await client.post(f"http://localhost:8000/distribucion/entregas/{entrega_id}/confirmar")
        assert response.status_code == 200

        # Check stock updated
        response = await client.get(f"http://localhost:8000/inventario/insumos/{insumo_id}")
        data = response.json()
        assert data["stock"]["actual"] == 5

        # Check entrega confirmed
        response = await client.get(f"http://localhost:8000/distribucion/entregas/{entrega_id}")
        data = response.json()
        assert data["estado"] == "CONFIRMADA"

        print("Integration test passed")

if __name__ == "__main__":
    asyncio.run(test_integration())