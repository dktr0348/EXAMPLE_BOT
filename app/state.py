from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    contact = State()
    location = State()
    age = State()
    photo = State()

class AddCategory(StatesGroup):
    name = State()
    sure = State()
   

class DeleteCategory(StatesGroup):
    select = State()
    sure = State()
   
class AddItem(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    sure = State()
   
class DeleteItem(StatesGroup):
    select = State()
    sure = State()
   