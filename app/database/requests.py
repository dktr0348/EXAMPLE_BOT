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
   