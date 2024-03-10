from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]

    subscriptions: Mapped[List["SubscriptionModel"]] = relationship(
        back_populates="user"
    )

    def __str__(self) -> str:
        return f"User {self.id} - {self.name}"

    def __repr__(self) -> str:
        return f"UserModel(id={self.id!r}, name={self.name!r})"


class ProductModel(Base):
    __tablename__ = "product"

    article: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    price: Mapped[int]
    sale_price: Mapped[int]
    rating: Mapped[int]
    count: Mapped[int]
    updated_by: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    subscriptions: Mapped[List["SubscriptionModel"]] = relationship(
        back_populates="product"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"Product(article={self.article}, name={self.name!r},"
            f" price={self.price!r}, sale_price={self.sale_price!r})"
        )

    class Meta:
        order_by = ["-updated_by"]


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    article_id: Mapped[int] = mapped_column(
        ForeignKey("product.article", ondelete="CASCADE")
    )

    user: Mapped["UserModel"] = relationship(back_populates="subscriptions")
    product: Mapped["ProductModel"] = relationship(back_populates="subscriptions")

    __table_args__ = (
        UniqueConstraint(
            "user_id", "article_id", name="unique_constraint_user_id_article_id"
        ),
    )

    def __str__(self) -> str:
        return f"User {self.user_id} subscribed on №{self.article_id}"

    def __repr__(self) -> str:
        return f"SubscriptionModel(user_id={self.user_id!r}, article_id={self.article_id!r})"
