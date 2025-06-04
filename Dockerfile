FROM python:3.12-slim

WORKDIR /doctors-appointment-notifier

COPY ./app ./doctors-appointment-notifier
COPY ./bot ./doctors-appointment-notifier
COPY ./external_sources_service ./doctors-appointment-notifier
COPY ./api.env ./doctors-appointment-notifier
COPY ./bot.env ./doctors-appointment-notifier
COPY ./init_service.py ./doctors-appointment-notifier
COPY ./start_api.py ./doctors-appointment-notifier
COPY ./start_bot.py ./doctors-appointment-notifier
COPY ./requirements.txt ./doctors-appointment-notifier
COPY ./start.sh ./doctors-appointment-notifier

RUN pip install --no-cache-dir --upgrade -r ./doctors-appointment-notifier/requirements.txt

CMD ["./start.sh"]