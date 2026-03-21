from pydantic import BaseModel, Field

class TokenRequest(BaseModel):
    token: str = Field(..., description="JWT Token del usuario logueado")
