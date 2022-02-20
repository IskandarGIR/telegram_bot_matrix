import logging
import numpy as np
from aiogram import Bot, Dispatcher, types
import config
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
#log level
logging.basicConfig(
    level=logging.INFO
)

#bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage = storage)



#start bot
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/mult", "Найти обратную матрицу"]
    keyboard.add(*buttons)
    await message.answer("Привет, {0}!".format(message.from_user.first_name)+" Что вы хотите?", reply_markup=keyboard)

class Mult(StatesGroup):
    size = State()
    matrix_1 = State()
    matrix_2 = State()


@dp.message_handler(Command("mult"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Введите размер матрицы(Например: \"2 2\")")
    await Mult.size.set()


@dp.message_handler(state=Mult.size)
async def answer_size(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1 = answer)

    await message.answer("Введите матрицу:")
    await Mult.next()


@dp.message_handler(state=Mult.matrix_1)
async def answer_matrix_1(message: types.Message, state: FSMContext):
    answer_2 = message.text
    await state.update_data(answer2=answer_2)
    await message.answer("Введите другую матрицу:")

    await Mult.next()

@dp.message_handler(state=Mult.matrix_2)
async def answer_matrix_1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1").split()
    answer2 = data.get("answer2").split()
    a1 = [int(i) for i in answer1]
    answer3 = message.text.split()
    a2 = [int(i) for i in answer2]
    a3 = [int(i) for i in answer3]

    v1 = np.array(a2)
    mat_1 = v1.reshape(a1)
    v2 = np.array(a2)
    mat_2 = v2.reshape(a1)
    await message.answer(mat_2.dot(mat_1))

    await state.finish()






@dp.message_handler(Text(equals="Умножить"))
async def with_puree(message: types.Message):
    await message.answer("Введите размер матрицы",reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Найти обратную матрицу"))
async def with_puree(message: types.Message):
    await message.answer("Введите размер матрицы",reply_markup=types.ReplyKeyboardRemove())

#run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)

