from pydantic import BaseModel
from typing import Optional

class SlotModel(BaseModel):
    date: str
    details: list['SlotDetailsModel']

class SlotDetailsModel(BaseModel):
    rid: int
    eid: int
    b_dt: str
    edate: str
    duration: int

class TokenModel(BaseModel):
    result: bool
    token: str
    name: str

class AuthResponseModel(BaseModel):
    message: str
    data : Optional[TokenModel] = None