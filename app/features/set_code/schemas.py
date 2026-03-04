from pydantic import BaseModel

class SetCodeRequest(BaseModel):
    code: str

class SetCodeResponse(BaseModel):
    success: bool
    message: str
    data: int