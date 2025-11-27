from .entities import Insumo

class ServicioValidacionStock:
    @staticmethod
    def validar(insumo: Insumo, cantidad: int) -> bool:
        return insumo.verificar_disponibilidad(cantidad)

class ServicioAjusteStock:
    @staticmethod
    def ajustar(insumo: Insumo, cantidad: int) -> None:
        insumo.descontar_stock(cantidad)