import logging

import aiohttp
from pydantic import BaseModel, Field

from bot.database.orm import ORM


class Product(BaseModel):
    article: int = Field(alias="id")
    name: str
    rating: int
    price_raw: int = Field(alias="priceU")
    sale_price_raw: int = Field(alias="salePriceU")
    count: int = Field(alias="wh")

    @property
    def price(self) -> int:
        return self.price_raw // 100

    @property
    def sale_price(self) -> int:
        return self.sale_price_raw // 100


class Data(BaseModel):
    products: list[Product]


class Raw(BaseModel):
    data: Data
    state: int


async def fetch_product(article: str) -> Product:
    async with aiohttp.ClientSession() as session:
        logging.info(f"Fetching product with article: {article}")
        request = await session.get(
            f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"  # TODO: Add a message broker
        )
        if request.status != 200:
            raise Exception(f"Invalid request with status code: {request.status}")
        try:
            data = Raw(**await request.json())
            product = data.data.products[0]
        except IndexError as e:
            pass
        logging.info(f"Fetched product, article: {product.article}")
        await ORM.insert_product(
            product.article,
            product.name,
            product.price,
            product.sale_price,
            product.rating,
            product.count,
        )
        logging.info(f"Product №{product.article} added to database")
        return product
