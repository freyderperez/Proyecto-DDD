class Cedula(str):
    def __new__(cls, value: str):
        if not value.strip():
            raise ValueError("Cedula cannot be empty")
        return super().__new__(cls, value.strip())

class EstadoEmpleado(str):
    def __new__(cls, value: str):
        if value not in ["activo", "inactivo"]:
            raise ValueError("Estado must be activo or inactivo")
        return super().__new__(cls, value)