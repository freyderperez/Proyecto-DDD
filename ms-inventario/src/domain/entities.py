from uuid import uuid4

from .value_objects import CantidadStock, Nombre, Categoria

class Insumo:
    def __init__(self, nombre: Nombre, categoria: Categoria, stock: CantidadStock, id=None):
        self.id = id if id is not None else uuid4()
        self.nombre = nombre
        self.categoria = categoria
        self.stock = stock

    def verificar_disponibilidad(self, cantidad: int) -> bool:
        return self.stock.actual >= cantidad

    def descontar_stock(self, cantidad: int) -> None:
        if cantidad > self.stock.actual:
            raise ValueError("Insufficient stock")
        self.stock = CantidadStock(
            actual=self.stock.actual - cantidad,
            min_=self.stock.min,
            max_=self.stock.max
        )

    def es_stock_critico(self) -> str:
        if self.stock.actual == 0:
            return "agotado"
        elif self.stock.actual < self.stock.min:
            return "bajo"
        elif self.stock.actual > self.stock.max:
            return "exceso"
        return "normal"