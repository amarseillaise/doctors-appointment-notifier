import os

import uvicorn
from fastapi import FastAPI, status

from app.api import service
from app.models import SlotModel

server = ...
app = FastAPI()

def run_uvicorn():
    global server
    config = {
        'app': app,
        'host': os.getenv('HOST'),
        'port': int(os.getenv('PORT')),
        'reload': True,
    }
    server = uvicorn.Server(uvicorn.Config(**config))
    server.run()

@app.get("/api/slots/",
         response_description='Returns a list of doctors slots',
         response_model=list[SlotModel],
         status_code=status.HTTP_200_OK)
def get_slots() -> list[SlotModel]:
    slots = service.get_slots()
    return slots