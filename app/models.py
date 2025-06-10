from pydantic import BaseModel
from typing import Optional

class TokenModel(BaseModel):
    result: bool
    token: str
    name: str


class AuthResponseModel(BaseModel):
    message: str
    data : Optional[TokenModel] = None


class SlotModel(BaseModel):
    date: str
    details: list['SlotDetailsModel']


class SlotDetailsModel(BaseModel):
    rid: int
    eid: int
    b_dt: str
    edate: str
    duration: int


class DoctorInfoModel(BaseModel):
    code: str
    name: str

class DoctorToSlotMapModel(BaseModel):
    doctor: DoctorInfoModel
    slots: list[SlotModel]