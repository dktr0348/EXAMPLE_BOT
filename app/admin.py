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
    await message.answer("Добро пожаловать в бот, администратор",
                         reply_markup=kb.admin_main)

@admin.message(Admin(), F.text == 'Выйти')
async def exit(message: Message):
    await message.answer("Вы вышли из режима администратора",
                         reply_markup=kb.main)


@admin.message(Admin(), F.text == 'Добавить категорию')
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
                                  reply_markup=kb.admin_main)
    await state.clear()

@admin.callback_query(Admin(),F.data =='cancel-sure', st.AddCategory.sure)
async def add_category_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Добавление категории отменено",
                                  reply_markup=kb.admin_main)
    await state.clear()

@admin.message(Admin(), F.text == 'Удалить категорию')
async def delete_category_select(message: Message, state: FSMContext):
    await state.set_state(st.DeleteCategory.select)
    keyboard = await kb.delete_categories()
    await message.answer("Выберети категорию для удаления:",
                         reply_markup=keyboard)
    
@admin.callback_query(F.data.startswith("delete_"))
async def process_category_selection(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.set_state(st.DeleteCategory.sure)
    await state.update_data(category_id=category_id)
    await callback.message.answer(f"Вы уверены, что хотите удалить эту категорию?",
                                reply_markup=kb.sure)

@admin.callback_query(Admin(),F.data =='ok-sure', st.DeleteCategory.sure)
async def delete_category_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.delete_category(data['category_id'])
    await callback.message.answer("Категория удалена",
                                  reply_markup=kb.admin_main)
    await state.clear()

@admin.message(Admin(), F.text == 'Добавить товар')
async def add_item(message: Message, state: FSMContext):
    await state.set_state(st.AddItem.category)
    keyboard = await kb.admin_categories()
    await message.answer("Выбрать категорию для добавления товара:",
                         reply_markup=keyboard)

@admin.callback_query(F.data.startswith("category_"), st.AddItem.category)
async def add_item_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category_id=callback.data.split("_")[1])
    await state.set_state(st.AddItem.name)
    await callback.message.answer("Введите название товара:")
    await callback.answer()
@admin.message(Admin(), st.AddItem.name)
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.AddItem.description)
    await message.answer("Введите описание товара:")

@admin.message(Admin(), st.AddItem.description)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(st.AddItem.price)
    await message.answer("Введите цену товара:")

@admin.message(Admin(), st.AddItem.price)
async def add_item_sure(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(st.AddItem.sure)
    data = await state.get_data()
    await message.answer(f"Вы уверены, что хотите добавить этот товар?\n\n"
                         f"Название: {data['name']}\n\n"
                         f"Описание: {data['description']}\n\n"
                         f"Цена: {data['price']}",
                         reply_markup=kb.sure)

@admin.callback_query(Admin(), F.data == 'ok-sure', st.AddItem.sure)
async def add_item_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await db.add_item(data['name'], data['description'], data['price'], data['category'])
    await callback.message.answer("Товар добавлен",
                                  reply_markup=kb.admin_main)
    await state.clear()

@admin.callback_query(Admin(), F.data == 'cancel-sure', st.AddItem.sure)
async def add_item_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Добавление товара отменено",
                                  reply_markup=kb.admin_main)
    await state.clear()

@admin.message(Admin(), F.text == 'Удалить товар')
async def delete_item_select(message: Message, state: FSMContext):
    await state.set_state(st.DeleteItem.select)
    keyboard = await kb.delete_items()
    await message.answer("Выберите товар для удаления:",
                         reply_markup=keyboard)
    

