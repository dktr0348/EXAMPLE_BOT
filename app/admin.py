from aiogram import F
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, BaseFilter
from config import ADMINS
import app.state as st
import app.keybords as kb
import app.database.requests as db
from aiogram.fsm.context import FSMContext

admin = Router()

class Admin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS
    
admin.message.filter(Admin())

@admin.message(Admin(), Command('admin'))
async def cmd_command(message: Message):
    await message.answer("Добро пожаловать в бот, администратор")

@admin.message(Admin(), Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    await state.set_state(st.AddCategory.name)
    await message.answer("Введите название категории:")

@admin.message(Admin(), st.AddCategory.name)
async def add_category_sure(message: Message, state: FSMContext):
    await state.set_state(st.AddCategory.sure)
    await state.update_data(name=message.text)
    await message.answer(f"Вы уверены, что хотите добавить категорию? - {message.text}",
                         reply_markup=kb.sure)

@admin.callback_query(Admin(),F.data =='ok-sure', st.AddCategory.sure)
async def add_category_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.add_category(data['name'])
    await callback.message.answer("Категория добавлена",
                                  reply_markup=kb.main)
    await state.clear()

@admin.callback_query(Admin(),F.data =='cancel-sure', st.AddCategory.sure)
async def add_category_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Добавление категории отменено",
                                  reply_markup=kb.main)
    await state.clear()
