from aiogram_dialog import DialogManager
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from bot.database import session, models


class ORM:
    @staticmethod
    async def insert_user(user_id: int, username: str):
        async with session() as conn:
            insert_stmt = insert(models.UserModel).values(id=user_id, name=username)
            update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["id"], set_=dict(name=username)
            )
            await conn.execute(update_stmt)
            await conn.commit()

    @staticmethod
    async def insert_product(
        article: int, name: str, price: int, sale_price: int, rating: int, count: int
    ):
        async with session() as conn:
            insert_stmt = insert(models.ProductModel).values(
                article=article,
                name=name,
                price=price,
                sale_price=sale_price,
                rating=rating,
                count=count,
            )
            update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["article"],
                set_=dict(
                    name=name,
                    price=price,
                    sale_price=sale_price,
                    rating=rating,
                    count=count,
                ),
            )
            await conn.execute(update_stmt)
            await conn.commit()

    @staticmethod
    async def get_last_5_products(dialog_manager: DialogManager, **kwargs):
        async with session() as conn:
            query = (
                select(models.ProductModel)
                .order_by(models.ProductModel.updated_by.desc())
                .limit(5)
            )
            results = await conn.execute(query)
            results = results.fetchall()
            return {"products": [product[0] for product in results]}

    @staticmethod
    async def insert_subscription(user_id: int, article_id: int):
        async with session() as conn:
            insert_stmt = insert(models.SubscriptionModel).values(
                user_id=user_id,
                article_id=article_id,
            )
            nothing_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=["user_id", "article_id"],
            )
            await conn.execute(nothing_stmt)
            await conn.commit()

    @staticmethod
    async def delete_subscriptions_for_user(user_id: int):
        async with session() as conn:
            delete_stmt = delete(models.SubscriptionModel).where(
                models.SubscriptionModel.user_id == user_id
            )
            await conn.execute(delete_stmt)
            await conn.commit()

    @staticmethod
    async def get_all_subscribers():
        async with session() as conn:
            query = select(models.SubscriptionModel).options(
                joinedload(models.SubscriptionModel.product)
            )
            results = await conn.execute(query)
            return results.scalars().all()
