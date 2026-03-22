from pydantic import BaseModel

class ChangePasswordRequest(BaseModel):
    token: str
    old_password: str
    new_password: str

class ChangePasswordResponse(BaseModel):
    success: bool
    message: str
