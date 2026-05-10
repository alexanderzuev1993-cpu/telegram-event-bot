import asyncio
import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

# ========== ТОКЕН И ЧАСОВОЙ ПОЯС ==========
TOKEN = "8603018277:AAGTYFChXE7cHJp24Z0lWOSDbA8xXxnq9ic"
TIMEZONE = pytz.timezone("Europe/Berlin")  # UTC+1

# ========== РАСПИСАНИЕ (полностью из вашего файла) ==========
SCHEDULE = [
    # Понедельник (0)
    (0, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (0, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (0, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (0, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (0, 20, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (20:00)"),
    (0, 21, 0, 10, "Через 10 минут/After 10 minutes: Якудза/Yakuza (21:00-21:40)"),
    # Вторник (1)
    (1, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (1, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (1, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (1, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (1, 20, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (20:00)"),
    (1, 20, 50, 10, "Через 10 минут/After 10 minutes: ГвГ/ClubWar (20:50)"),
    (1, 21, 20, 5, "Через 5 минут/After 5 minutes: Ужин, Звезда, Сила/Feast, Star, POC (21:20)"),
    # Среда (2)
    (2, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (2, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (2, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (2, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (2, 20, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (20:00)"),
    (2, 21, 0, 10, "Через 10 минут/After 10 minutes: Хякки/HauntedNight (21:00)"),
    (2, 21, 30, 5, "Через 5 минут/After 5 minutes: Арена/Arena (21:30)"),
    # Четверг (3)
    (3, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (3, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (3, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (3, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (3, 20, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (20:00)"),
    (3, 20, 50, 10, "Через 10 минут/After 10 minutes: ГвГ/ClubWar (20:50)"),
    (3, 21, 25, 10, "Через 10 минут/After 10 minutes: ПБМ(1-й и 2-й заход)/COS(1th and 2nd run) (21:25)"),
    (3, 21, 35, 5, "Через 5 минут/After 5 minutes: Ужин, Звезда, Сила/Feast, Star, POC (21:35)"),
    # Пятница (4)
    (4, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (4, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (4, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (4, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (4, 19, 0, 10, "Через 10 минут/After 10 minutes: Арес/Ares (19:00)"),
    (4, 20, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (20:00)"),
    (4, 20, 10, 5, "Регаем Дворец/Reg Palace (20:10)"),
    (4, 20, 30, 5, "Через 10 минут/After 10 minutes: ПБМ(3-й заход)/COS(3rd run) (20:30)"),
    (4, 20, 55, 10, "Регаем Дворец/Reg Palace (20:55)"),
    (4, 22, 0, 5, "Через 5 минут/After 5 minutes: Война клуба открыта/BattleSim opens (22:00)"),
    # Суббота (5)
    (5, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (5, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (5, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (5, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (5, 18, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (18:00)"),
    (5, 19, 30, 15, "Через 15 минут/After 15 minutes: Дракон на базе/DragonBreath (19:30)"),
    (5, 20, 55, 10, "Через 10 минут/After 10 minutes: Срочно!Охрана/DefendBoss (20:55)"),
    (5, 21, 20, 5, "Через 5 минут/After 5 minutes: Токио/Tokyo (21:20)"),
    # Воскресенье (6)
    (6, 12, 30, 10, "Через 10 минут/After 10 minutes: Клуп/Clup (12:30-12:50)"),
    (6, 13, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (13:00)"),
    (6, 15, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (15:00)"),
    (6, 17, 0, 5, "Через 5 минут/After 5 minutes: Чизуру/Chizuru (17:00)"),
    (6, 18, 45, 5, "Кирли позорник"),
    (6, 19, 0, 5, "Через 5 минут/After 5 minutes: Чизуру меж/Chizuru cross (19:00)"),
    (6, 19, 30, 10, "Через 10 минут/After 10 minutes: Война ветров/ServerWar (19:30)"),
    (6, 20, 40, 5, "Через 5 минут/After 5 minutes: Звезда/Chizuru Star (20:40)"),
    (6, 21, 0, 10, "Через 10 минут/After 10 minutes: Бомбы/Bombs (21:00)"),
]

# ========== КОД БОТА (НЕ ТРОГАТЬ) ==========
bot = Bot(token=TOKEN)
dp = Dispatcher()

GROUP_ID = None
THREAD_ID = None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Бот запущен. Используйте /setthread в нужной ветке.")

@dp.message(Command("setthread"))
async def set_thread(message: types.Message):
    global GROUP_ID, THREAD_ID
    GROUP_ID = message.chat.id
    if message.message_thread_id:
        THREAD_ID = message.message_thread_id
        await message.answer(f"✅ Ветка сохранена! Уведомления будут сюда.")
    else:
        await message.answer("❌ Напишите эту команду внутри ветки (не в основном чате).")

async def check_and_send():
    global GROUP_ID, THREAD_ID
    if GROUP_ID is None or THREAD_ID is None:
        return
    now = datetime.datetime.now(TIMEZONE)
    wd = now.weekday()
    h = now.hour
    m = now.minute
    for weekday, hour, minute, offset, text in SCHEDULE:
        if weekday != wd:
            continue
        send_h = hour
        send_m = minute - offset
        if send_m < 0:
            send_h -= 1
            send_m += 60
        if send_h < 0:
            send_h += 24
        if send_h == h and send_m == m:
            try:
                await bot.send_message(chat_id=GROUP_ID, message_thread_id=THREAD_ID, text=text)
                print(f"Отправлено: {text}")
            except Exception as e:
                print(f"Ошибка: {e}")

async def scheduler():
    while True:
        await check_and_send()
        await asyncio.sleep(60)

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="setthread", description="Установить эту ветку для уведомлений"),
    ])
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(main())
