from aiogram.types import (KeyboardButton , ReplyKeyboardMarkup,
                            InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import app.database.requests as db

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')], 
    [KeyboardButton(text='Корзина')]],
    resize_keyboard=True)

async def categories():
    all_categories = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return keyboard.adjust(2).as_markup()

async def category_items(category_id):
    all_items = await db.get_items_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    return keyboard.adjust(2).as_markup()

sure = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='ok-sure')], 
    [InlineKeyboardButton(text='Нет', callback_data='cancel-sure')]],
    resize_keyboard=True)

admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить категорию', callback_data='add_category'), 
    KeyboardButton(text='Удалить категорию', callback_data='delete_category')],
    [KeyboardButton(text='Добавить товар', callback_data='add_item'), 
    KeyboardButton(text='Удалить товар', callback_data='delete_item')],
    [KeyboardButton(text='Добавить админа', callback_data='add_admin'), 
    KeyboardButton(text='Удалить админа', callback_data='delete_admin')],
    [KeyboardButton(text='Выйти', callback_data='exit')],
    ],
    resize_keyboard=True)

async def delete_categories():
    all_categories = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'delete_{category.id}'))
    return keyboard.adjust(2).as_markup()

async def admin_categories():
    all_categories = await db.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return keyboard.adjust(2).as_markup()