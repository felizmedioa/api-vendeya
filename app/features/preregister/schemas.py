from pydantic import BaseModel

class SendRequest(BaseModel):
    converted: bool
    send: bool