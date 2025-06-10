import os

from utils import DataPacker
from external_sources_service.target_site_worker import RequestWorker
from fastapi import HTTPException
from app.models import DoctorToSlotMapModel


def _get_target_site_worker() -> RequestWorker:
    username = os.getenv('USERNAME')
    passwd = os.getenv('PASSWORD')
    doctor_infos = _parse_doctors_code(os.getenv('DOCTORS_INFO'))
    return RequestWorker(username, passwd, doctor_infos)

def _parse_doctors_code(codes: str) -> list[dict]:
    parsed_string = codes.split(';')
    result = [dict(code=infos.split(':')[0], name=infos.split(':')[1])
              for infos in parsed_string]
    return result


def _authenticate(target_site_worker: RequestWorker) -> None:
    if not target_site_worker.authenticate():
        raise HTTPException(401)


def get_slots() -> list[DoctorToSlotMapModel]:
    site_worker = _get_target_site_worker()
    raw_slots = site_worker.get_slots()
    data_packer = DataPacker()
    formated_slots = data_packer.get_packed_slots(raw_slots)
    return formated_slots
