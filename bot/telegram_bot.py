import telebot
import os


from init_service import init_env_vars
from bot.bot_service import DoctorAppointmentBotService

init_env_vars('bot.env')
current_thread = ...
bot_service = DoctorAppointmentBotService()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    bot_service.start(message.chat)

@bot.message_handler(commands=['stop'])
def stop(message):
    bot_service.stop(message.chat)

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    bot_service.subscribe(bot, message)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    bot_service.unsubscribe(bot, message)

@bot.message_handler(commands=['list_slots'])
def list_slots(message):
    bot_service.send_list_slots(bot, message)

@bot.message_handler(commands=['try_set_day_delta'])
def try_set_day_delta(message):
    bot_service.try_set_day_delta(bot, message)

def main():
    bot_service.init_commands(bot)
    if bot_service.check_start_site_polling():
        bot_service.start_polling(bot)
    bot.infinity_polling()

if __name__ == "__main__":
    main()

