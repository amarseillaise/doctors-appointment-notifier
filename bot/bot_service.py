import sys
import schedule
import time
import json
import os
import logging
from logging import FileHandler
from datetime import datetime
from threading import Thread

from telebot import TeleBot, types, apihelper

from bot.http_service import DoctorsAppointmentHttpService
from app.models import DoctorToSlotMapModel

current_thread = ...


class DoctorAppointmentBotService:

    def __init__(self):
        self.polling_site_enabled = False
        self.all_slot_list = []
        self.current_max_day_delta = 7
        self.http_service = DoctorsAppointmentHttpService()
        self.logger = logging.getLogger('main')
        self.logger.addHandler(FileHandler('./log.log', 'a', 'utf-8'))

    def init_commands(self, bot: TeleBot):
        commands = [
            types.BotCommand('subscribe', description='Подписаться на освободившиеся слоты'),
            types.BotCommand('unsubscribe', description='Отписаться от освободившихся слотов'),
            types.BotCommand('list_slots', description='Список всех временных слотов'),
            types.BotCommand('set_new_day_delta_handler', description='Задать максимальную дельту в днях для отслеживания слотов'),
        ]
        bot.set_my_commands(commands)

    def start(self, chat: types.Chat):
        pass

    def stop(self, chat: types.Chat):
        self._remove_user_from_subscribers(chat.id)

    def subscribe(self, bot: TeleBot, chat_message: types.Message):
        global current_thread
        self._add_user_to_subscribers(chat_message.chat.id, chat_message.chat.username)
        bot.send_message(chat_message.chat.id, 'При появлении свободного слота, придёт уведомление')
        if self.check_start_site_polling():
            self.start_polling(bot)

    def set_new_day_delta_handler(self, bot: TeleBot, chat_message: types.Message):
        bot.send_message(chat_message.chat.id, 'Введи значение')
        bot.register_next_step_handler(chat_message, self.try_set_day_delta, bot=bot)

    def try_set_day_delta(self, chat_message: types.Message, bot: TeleBot):
        new_delta = self._verify_day_delta_value(chat_message.text)
        if new_delta > 0:
            self.current_max_day_delta = new_delta
            msg = 'Новая дельта сохранена'
            bot.send_message(chat_message.chat.id, msg)
        else:
            msg = 'Значение должно быть числом и должно быть больше нуля'
            bot.send_message(chat_message.chat.id, msg)

    def _verify_day_delta_value(self, value: str):
        try:
            verified_delta = int(value)
        except ValueError:
            verified_delta = -1
        return verified_delta

    def _add_user_to_subscribers(self, user_id, user_name) -> None:
        subscribers = self._get_subscribers()
        subscribers[str(user_id)] = str(user_name)
        self._write_subscribers(subscribers)

    def unsubscribe(self, bot: TeleBot, chat_message: types.Message):
        self._remove_user_from_subscribers(chat_message.chat.id)
        bot.send_message(chat_message.chat.id, 'Свободные слоты больше не отслеживаются')

    def send_list_slots(self, bot: TeleBot, chat_message: types.Message):
        slots = self.http_service.get_slot_list()
        message = self._get_all_slots_formated(slots)
        if message:
            bot.send_message(chat_message.chat.id, message)
        else:
            photo = open('static/okak.jpg', 'rb')
            caption = 'А свободных мест то и нет'
            bot.send_photo(chat_message.chat.id, photo, caption)
            photo.close()

    def check_start_site_polling(self) -> bool:
        return self._has_subscribers() and not self.polling_site_enabled

    def _check_slots_available(self, bot: TeleBot):
        available_slots = self.http_service.get_slot_list()
        nearest_doctor = self._get_nearest_doctor(available_slots)
        self.logger.info(nearest_doctor)
        if nearest_doctor:
            message = self._get_available_slots_formated(nearest_doctor)
            self._send_message_to_subscribers(message, bot)

    def _get_nearest_doctor(self, available_slots) -> DoctorToSlotMapModel | None:
        nearest_delta = sys.maxsize
        nearest_doctor = None
        for doctor in available_slots:
            date = doctor.slots[0].date
            delta = self._compute_delta(date)
            if self._is_delta_ok(date) and delta < nearest_delta:
                nearest_delta = delta
                nearest_doctor = doctor
        return nearest_doctor

    def _is_delta_ok(self, target_day: str) -> bool:
        delta = self._compute_delta(target_day)
        return delta <= self.current_max_day_delta

    def _compute_delta(self, day: str) -> int:
        nearest_date_lst = list(map(int, day.split('.')))
        nearest_date_lst.reverse()
        nearest_date = datetime(*nearest_date_lst)
        return (nearest_date - datetime.now()).days

    def start_polling(self, bot: TeleBot):
        global current_thread
        current_thread = Thread(target=self._run_thread_polling, kwargs={'bot': bot})
        current_thread.start()

    def _run_thread_polling(self, bot: TeleBot):
        timeout = int(os.getenv('POLLING_TIMEOUT_MINUTES'))
        job = schedule.every(timeout).minutes.do(self._check_slots_available, bot=bot)
        while self._has_subscribers():
            self.polling_site_enabled = True
            schedule.run_pending()
            time.sleep(1)
        self.polling_site_enabled = False
        schedule.cancel_job(job)

    def _send_message_to_subscribers(self, message: str, bot: TeleBot):
        subscribers = self._get_subscribers()
        for subscriber_id in subscribers.keys():
            try:
                bot.send_message(subscriber_id, message)
            except apihelper.ApiTelegramException:
                self._remove_user_from_subscribers(subscriber_id)
            finally:
                continue

    def _remove_user_from_subscribers(self, user_id) -> None:
        subscribers = self._get_subscribers()
        subscribers.pop(str(user_id), None)
        self._write_subscribers(subscribers)

    def _has_subscribers(self) -> bool:
        return bool(self._get_subscribers())

    @staticmethod
    def _get_subscribers() -> dict:
        file_path = './subscribers.json'
        if not os.path.exists(file_path):
            return {}
        with open(file=file_path, mode='r') as f:
            content = f.read()
            return json.loads(content)

    @staticmethod
    def _write_subscribers(data: dict) -> None:
        file_path = './subscribers.json'
        with open(file=file_path, mode='w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def _get_all_slots_formated(slots: list[DoctorToSlotMapModel]) -> str:
        msg = ''
        if slots:
            msg = 'Для записи доступны следующие докторы и даты даты:\n'
            for slot in slots:
                msg += f'\n{slot.doctor.name}:\n'
                for day in slot.slots:
                    msg += f'{day.date}\n'
        return msg

    @staticmethod
    def _get_available_slots_formated(nearest_day: DoctorToSlotMapModel) -> str:
        text = 'Срочно! Срочно! Срочно! Доступна запись:'
        doctors_name = nearest_day.doctor.name
        day = nearest_day.slots[0].date
        _time = nearest_day.slots[0].details[0].b_dt

        return f'{text}\n\n{doctors_name}:\n{day} - {_time}'
