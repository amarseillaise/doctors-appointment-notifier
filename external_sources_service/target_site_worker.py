import requests
import json
from dataclasses import dataclass
from functools import wraps
from typing import Callable

from app import models
from fake_useragent import UserAgent

class RequestWorker:

    def __init__(self, username: str, password: str, doctors_code:str):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.doctors_code = doctors_code
        self.token = None
        self.url = RequestWorker.Url()
        self._init_headers()

    def _auth_if_need(func: Callable):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            http_method = 'timetable-doctors'
            url = self._build_url(self.url.get_url(), http_method)
            body = json.dumps({'code': self.doctors_code})
            http_response = self.session.post(url, data=body, allow_redirects=False)
            if http_response.status_code in (302, 401):
                self.authenticate()
            return func(self, *args, **kwargs)


        return wrapper

    def authenticate(self):
        http_method = 'login'
        url = self._build_url(self.url.get_url(), http_method)
        http_response = self.session.post(url=url, data=self._get_raw_auth_data())
        if http_response.status_code == 200:
            response_model = models.AuthResponseModel(**json.loads(http_response.content))
            if response_model.data:
                self._set_bearer_token(response_model.data.token)
                return True

    @_auth_if_need
    def get_slots(self) -> dict:
        http_method = 'timetable-doctors'
        url = self._build_url(self.url.get_url(), http_method)
        body = json.dumps({'code': self.doctors_code})
        http_response = self.session.post(url, data=body)
        if http_response.status_code == 200:
            slots = json.loads(http_response.content)
            return slots
        return {}


    def _get_auth_data(self) -> dict[str, str]:
        return {'email': self.username, 'password': self.password}

    def _get_raw_auth_data(self) -> str:
        return json.dumps(self._get_auth_data())

    def _finish_worker_session(self) -> None:
        self.session.close()

    def _set_bearer_token(self, token) -> None:
        self.token = token
        self.session.headers['Authorization'] = f'Bearer {token}'

    def _init_headers(self):
        headers = {
            'accept': 'application/json',
            'accept-language': 'ru,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome
        }
        self.session.headers.update(headers)

    @staticmethod
    def _build_url(base_url: str, method: str):
        return f'{base_url}/{method}'

    @dataclass
    class Url:
        protocol = 'https'
        domain = 'api-lk.fnkc-fmba.ru'
        api = 'api'

        def get_url(self) -> str:
            return f'{self.protocol}://{self.domain}/{self.api}'