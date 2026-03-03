from pydantic import BaseModel


class TerminalFiltered(BaseModel):
    id: int
    nombre: str
    nombre_resumido: str


class TerminalList(BaseModel):
    list: list[TerminalFiltered]