from .entities import Empleado

class ServicioValidacionEmpleado:
    @staticmethod
    def validar(empleado: Empleado) -> bool:
        return empleado.es_activo()