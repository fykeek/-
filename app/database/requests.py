from app.database.models import async_session
from app.database.models import User, Category, Item, Number
from sqlalchemy import select

async def set_user(tg_id, tg_us):
    async with async_session() as seesion:
        user = await seesion.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            seesion.add(User(tg_id=tg_id, tg_username=tg_us))
            await seesion.commit()

async def set_num(tg_num, tg_name, tg_us):
    async with async_session() as seesion:
        seesion.add(Number(tg_name=tg_name, number=tg_num, tg_username=tg_us))
        await seesion.commit()

async def get_cat():
    async with async_session() as seesion:
        return await seesion.scalars(select(Category))

async def get_cat_Item(category_id):
    async with async_session() as seesion:
        return await seesion.scalars(select(Item).where(Item.category == category_id))

async def get_item(item_id):
    async with async_session() as seesion:
        return await seesion.scalar(select(Item).where(Item.id == item_id))
