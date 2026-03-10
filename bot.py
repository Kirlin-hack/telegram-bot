import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8663768812:AAHRON2oY0f_L2vXFP7QMm9uBRghol7lcfg"
ADMIN_IDS = [8167634087]  

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

questions = [
"1. Используете ли вы сложный пароль (буквы разного регистра, цифры, символы)?",
"2. Применяете ли вы разные пароли для разных сайтов и сервисов?",
"3. Включена ли у вас двухфакторная аутентификация?",
"4. Проверяете ли вы адрес сайта перед вводом личных данных?",
"5. Переходите ли вы по ссылкам из подозрительных сообщений?",
"6. Публикуете ли вы в социальных сетях личную информацию(адрес, номертелефона)?",
"7. Принимаете ли вы в друзья незнакомых людей?",
"8. Проверяете ли вы настройки приватности своих аккаунтов?",
"9. Используете ли вы антивирусное программное обеспечение?",
"10. Подключаетесь ли вы к открытым сетям Wi-Fi для ввода личныхданных?",
"11. Знаете ли вы, что такое фишинг и как его распознать?",
"12. Сохраняете ли вы пароли в открытом доступе (в заметках, на фото)?",
"13. Выходите ли вы из аккаунтов при использовании чужих устройств?",
"14. Сообщаете ли вы взрослым или в службу поддержки о подозрительныхситуациях?",
"15. Задумываетесь ли вы о последствиях перед публикациейфотографийиинформации?"
]

answers = {"Да":2, "Иногда":1, "Нет":0}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Иногда")],
        [KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
)

class TestStates(StatesGroup):
    question = State()

results = {}

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.update_data(score=0, q_index=0)
    await message.answer(questions[0], reply_markup=keyboard)
    await state.set_state(TestStates.question)

@dp.message(TestStates.question)
async def answer(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("q_index", 0)
    score = data.get("score", 0)

    if message.text in answers:
        score += answers[message.text]

    q_index += 1
    await state.update_data(score=score, q_index=q_index)

    if q_index < len(questions):
        await message.answer(questions[q_index], reply_markup=keyboard)
    else:
       
        if score <= 15:
            level = "Низкий уровень безопасности"
            rec = "• создать сложные уникальные пароли; • включить двухфакторную аутентификацию; • удалить лишнюю личную информацию из открытого доступа; • быть осторожным при получении сообщений от незнакомых пользователей;• не использовать открытые Wi-Fi сети для ввода конфиденциальныхданных"
        elif score <= 24:
            level = "Средний уровень безопасности"
            rec = "• усилить защиту аккаунтов; • регулярно проверять настройки приватности; • использовать антивирусное программное обеспечение; • избегать перехода по сомнительным ссылкам"
        else:
            level = "Высокий уровень безопасности"
            rec = "• продолжать соблюдать правила интернет-безопасности; • регулярно обновлять пароли; • делиться знаниями о цифровой безопасности с окружающими"

        await message.answer(f"Тест завершён\nВаш результат: {score}/30\nУровень: {level}\nРекомендация:\n{rec}")
        await state.clear()

       
        results[message.from_user.id] = {
            "score": score,
            "level": level,
            "name": message.from_user.full_name
        }

@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещён ❌")
        return

    if not results:
        await message.answer("Пока нет результатов.")
        return

    text = "Результаты пользователей:\n\n"
    for uid, data in results.items():
        text += f"{data['name']} — {data['score']}/30 — {data['level']}\n"
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())