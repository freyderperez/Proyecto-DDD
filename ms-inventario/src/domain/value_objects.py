from typing import NamedTuple

class CantidadStock(NamedTuple):
    actual: int
    min: int
    max: int

    def __new__(cls, actual: int, min_: int, max_: int):
        if actual < 0 or min_ < 0 or max_ < 0:
            raise ValueError("Stocks cannot be negative")
        return super().__new__(cls, actual, min_, max_)

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