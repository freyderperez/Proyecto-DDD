class CantidadSolicitada(int):
    def __new__(cls, value: int):
        if value <= 0:
            raise ValueError("Cantidad must be positive")
        return super().__new__(cls, value)

class EstadoEntrega(str):
    def __new__(cls, value: str):
        if value not in ["PENDIENTE", "CONFIRMADA"]:
            raise ValueError("Estado must be PENDIENTE or CONFIRMADA")
        return super().__new__(cls, value)