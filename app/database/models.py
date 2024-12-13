import sqlite3
from typing import List
from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import DB_URL


engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    age: Mapped[int]
    basket: Mapped[List['Basket']] = relationship(back_populates='user')

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    item: Mapped[List['Item']] = relationship(back_populates='category')

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[str] = mapped_column(String(10))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='item')
    basket: Mapped[List['Basket']] = relationship(back_populates='item')

class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    user: Mapped['User'] = relationship(back_populates='basket')
    item: Mapped['Item'] = relationship(back_populates='basket')

async def async_main(): 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)