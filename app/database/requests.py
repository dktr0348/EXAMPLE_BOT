from app.database.models import async_session
from app.database.models import Category, User, Item, Basket
from sqlalchemy import select, update, delete

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
   
async def get_items_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category_id==category_id))
   
async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id==item_id))
   