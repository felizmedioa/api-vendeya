from pydantic import BaseModel

class GetKeyRequest(BaseModel):
    idose: int

class SetKeyRequest(BaseModel):
    idose: int
    guia: str
    code: str
    password: str