import os

from external_sources_service.target_site_worker import RequestWorker
from fastapi import HTTPException
from app.models import SlotModel, SlotDetailsModel


def _get_target_site_worker() -> RequestWorker:
    username = os.getenv('USERNAME')
    passwd = os.getenv('PASSWORD')
    doctors_code = os.getenv('DOCTORS_CODE')
    return RequestWorker(username, passwd, doctors_code)


def _authenticate(target_site_worker: RequestWorker) -> None:
    if not target_site_worker.authenticate():
        raise HTTPException(401)


def get_slots() -> list[SlotModel]:
    site_worker = _get_target_site_worker()
    return [SlotModel(date=day, details=[SlotDetailsModel(**d) for d in ds])
            for day, ds in site_worker.get_slots().items()]
