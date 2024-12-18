from app.database.models import async_session
from app.database.models import Category, User, Item, Basket
from sqlalchemy import select, update, delete
from functools import wraps

def connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

@connection
async def get_categories(session):
    return await session.scalars(select(Category))
   
@connection
async def get_items_by_category(session, category_id):
    return await session.scalars(select(Item).where(Item.category_id==category_id))
   
@connection
async def get_item(session, item_id):
    return await session.scalar(select(Item).where(Item.id==item_id))
   
@connection
async def add_category(session, name: str):
    category = Category(name=name)
    session.add(category)
    await session.commit()
    return category
   
@connection
async def delete_category(session, category_id: int):
    await session.execute(delete(Category).where(Category.id==category_id))
    await session.commit()

@connection
async def add_item(session, name: str, description: str, price: str, category_id: int):
    item = Item(name=name, description=description, price=price, category_id=category_id)
    session.add(item)
    await session.commit()
    return item

@connection
async def delete_item(session, item_id: int):
    await session.execute(delete(Item).where(Item.id==item_id))
    await session.commit()

