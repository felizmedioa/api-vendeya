from pydantic import BaseModel

class TerminalList(BaseModel):
    list: list[TerminalFiltered]

class TerminalFiltered(BaseModel):
    id: int
    nombre: str
    nombre_resumido: str    