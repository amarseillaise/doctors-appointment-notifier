import requests
import json
from dataclasses import dataclass
from logging import log

from app.models import SlotModel, SlotDetailsModel

class DoctorsAppointmentHttpService:

    def __init__(self):
        self._url = self.Url()

    def get_slot_list(self) -> list[SlotModel]:
        http_method = 'slots/'
        response = self._get(http_method)
        if not response:
            return []
        return [SlotModel(date=slot['date'], details=[SlotDetailsModel(**ds) for ds in slot['details']])
                for slot in json.loads(response.content)]

    def _get(self, method_uri) -> requests.Response | None:
        url = f'{self._url.get_url()}/{method_uri}'
        response = self._make_request(requests.get, url=url)
        return response

    def _make_request(self, method, **kwargs) -> requests.Response | None:
        response = self._try_request(method, **kwargs)
        if response and response.status_code != 200:
            return None
        return response

    def _try_request(self, method, **kwargs) -> requests.Response | None:
        try:
            return method(**kwargs)
        except Exception as e:
            log(0, str(e), exc_info=e)
            return None

    @dataclass
    class Url:
        protocol = 'http'
        domain = '127.0.0.1'
        port = '2444'
        api = 'api'

        def get_url(self) -> str:
            return f'{self.protocol}://{self.domain}:{self.port}/{self.api}'