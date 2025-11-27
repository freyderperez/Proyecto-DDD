import requests
import time
import uuid

def test_integration():
    insumo_id = str(uuid.uuid4())
    empleado_id = str(uuid.uuid4())
    entrega_id = str(uuid.uuid4())

    # Health checks
    services = [8000, 8001, 8002, 8003]
    for port in services:
        response = requests.get(f"http://localhost:{port}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    # Create insumo (mock, since no POST endpoint yet)
    # Assume insumo created with stock 10 via direct DB or mock

    # Solicitar entrega
    response = requests.post("http://localhost:8003/api/v1/entregas", json={
        "id": entrega_id,
        "empleado_id": empleado_id,
        "insumo_id": insumo_id,
        "cantidad": 5
    })
    assert response.status_code == 200

    # Wait for async processing
    time.sleep(10)

    # Check stock in ms-inventario
    response = requests.get(f"http://localhost:8001/api/v1/insumos/{insumo_id}")
    data = response.json()
    assert data["stock_actual"] == 5

    # Check entrega status
    response = requests.get(f"http://localhost:8003/api/v1/entregas/{entrega_id}")
    data = response.json()
    assert data["estado"] == "CONFIRMADA"

    print("Integration test passed")

if __name__ == "__main__":
    test_integration()