from pydantic import BaseModel

class RegisterRequest(BaseModel):
    serviceOrder: list[int]
