from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import config

DATABASE_URL = f"sqlite+aiosqlite:///{config.db_path}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    weight_categories: Mapped[list["WeightCategory"]] = relationship(
        back_populates="vehicle_type", cascade="all, delete-orphan"
    )


class WeightCategory(Base):
    __tablename__ = "weight_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_type_id: Mapped[int] = mapped_column(ForeignKey("vehicle_types.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    city_price: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_km: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    vehicle_type: Mapped["VehicleType"] = relationship(back_populates="weight_categories")


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    vehicle_type: Mapped[str] = mapped_column(String(100), nullable=False)
    weight_category: Mapped[str] = mapped_column(String(100), nullable=False)
    trip_type: Mapped[str] = mapped_column(String(20), nullable=False)
    km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    calculated_price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
