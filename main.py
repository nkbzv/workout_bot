from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN_API
import markups as mu
from db_fuctions import create_connection, add_user_max, add_next_trainings, add_training, get_user_info, get_next_training
from calc_trains import calc_trains
from tabulate import tabulate
import time
import string
import random

HELP_COMMAND = """
/start - Начать работу с ботом;
/help - Список комманд."""
GREET_TEXT = 'Привет! \nЯ бот для тренировок, и моя главная цель - помочь \
тебе стать более здоровым и улучшить свою физическую форму. Я создан для \
того, чтобы помочь тебе достичь целей в 200 отжиманий, 200 скручиваний и 10 \
минут в планке. Мой алгоритм работы основан на твоих возможностях, и я создаю \
индивидуальные тренировочные планы, которые помогут тебе развить силу и выносливость. \
\nДавай вместе достигнем желаемых результатов!'
ABOUT_TEXT = 'Данный бот создан Кобзевым Никитой @kbzvspb'
COUNT = 0


storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

class MaxReps(StatesGroup):
    waiting_for_max_reps = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text=GREET_TEXT, parse_mode='HTML', reply_markup = mu.mainMenu)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
    await message.delete()

@dp.message_handler(text=['🏠 Главное меню'])
async def mainmenu_button(message: types.Message):
    await message.answer('🏠 Главное меню', reply_markup=mu.mainMenu)

@dp.message_handler(text=['💪 Тренировки'])
async def trainmenu_button(message: types.Message):
    await message.answer('Выберите тренировку:', reply_markup=mu.workoutMenu)

@dp.message_handler(text=['🚸 Другое'])
async def othermenu_button(message: types.Message):
    await message.answer('🚸 Другое', reply_markup=mu.otherMenu)

@dp.message_handler(text=['🥇 200 pushups', '🥈 200 crunches', '🥉 10 minute planka'])
async def curtrainmenu_button(message: types.Message, state: FSMContext):
    cur_train = message.text.split()[-1]
    user_id = message.from_user.id
    await state.update_data(cur_train=cur_train, user_id=user_id)
    with create_connection() as conn:
        user_info = get_user_info(conn, user_id, cur_train)
        if "message" in user_info and user_info["max_reps"] == 0:
            await message.answer(user_info["message"])
            await MaxReps.waiting_for_max_reps.set()
        else:
            await message.answer("Выберите действие:", reply_markup=mu.curtrainMenu)

    @dp.message_handler(text='🫡 Начать тренировку')
    async def start_training(message: types.Message):
        pass

    @dp.message_handler(text='📊 История тренировок')
    async def training_history(message: types.Message):
        pass

@dp.message_handler(state=MaxReps.waiting_for_max_reps)
async def max_reps_input(message: types.Message, state: FSMContext):
    data = await state.get_data() 
    user_id = data.get("user_id")
    cur_train = data.get("cur_train")
    
    try:
        max_reps = int(message.text)
        await state.update_data(max_reps=max_reps)
        if max_reps <= 0:
            await message.answer("Максимум должен быть положительным числом. Введите еще раз.")
            #await MaxReps.waiting_for_max_reps.set()
        else:
            with create_connection() as conn:
                add_user_max(conn, user_id, cur_train, max_reps)
                time.sleep(2)
                await message.answer(f"Ваш максимум на данный момент: {max_reps} {cur_train}", reply_markup=mu.curtrainMenu)
                await message.answer('Вам составлен план на три тренировки:')
                data = await state.get_data()
                max_reps = data.get("max_reps")
                trains = calc_trains(max_reps)
                header = ["1", "2", "3"]
                rows = []
                for i, train in enumerate(trains):
                    row_name = f"Подход {i+1}"
                    for j, set in enumerate(train):
                        rows.append([row_name] + set)

                table = tabulate(rows, headers=header, tablefmt="pipe")
                await message.answer(table)
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите целое положительное число:")
        await MaxReps.waiting_for_max_reps.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

