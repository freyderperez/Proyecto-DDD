from dataclasses import dataclass

@dataclass(frozen=True)
class CantidadStock:
    actual: int
    min: int
    max: int

    def __post_init__(self):
        if self.actual < 0 or self.min < 0 or self.max < 0:
            raise ValueError("Stocks cannot be negative")

class Nombre(str):
    def __new__(cls, value: str):
        if not value.strip():
            raise ValueError("Nombre cannot be empty")
        return super().__new__(cls, value.strip())

class Categoria(str):
    def __new__(cls, value: str):
        if not value.strip():
            raise ValueError("Categoria cannot be empty")
        return super().__new__(cls, value.strip())