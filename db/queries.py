from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from db.models import Request, VehicleType, WeightCategory, async_session


# ---------- Vehicle types ----------

async def get_active_vehicle_types() -> list[VehicleType]:
    async with async_session() as session:
        result = await session.execute(
            select(VehicleType).where(VehicleType.is_active.is_(True)).order_by(VehicleType.id)
        )
        return list(result.scalars().all())


async def get_all_vehicle_types() -> list[VehicleType]:
    async with async_session() as session:
        result = await session.execute(select(VehicleType).order_by(VehicleType.id))
        return list(result.scalars().all())


async def get_vehicle_type_by_id(vehicle_id: int) -> VehicleType | None:
    async with async_session() as session:
        return await session.get(VehicleType, vehicle_id)


async def create_vehicle_type(name: str) -> VehicleType:
    async with async_session() as session:
        vehicle = VehicleType(name=name, is_active=True)
        session.add(vehicle)
        await session.commit()
        await session.refresh(vehicle)
        return vehicle


async def rename_vehicle_type(vehicle_id: int, new_name: str) -> None:
    async with async_session() as session:
        vehicle = await session.get(VehicleType, vehicle_id)
        if vehicle:
            vehicle.name = new_name
            await session.commit()


async def deactivate_vehicle_type(vehicle_id: int) -> None:
    async with async_session() as session:
        vehicle = await session.get(VehicleType, vehicle_id)
        if vehicle:
            vehicle.is_active = False
            result = await session.execute(
                select(WeightCategory).where(WeightCategory.vehicle_type_id == vehicle_id)
            )
            for category in result.scalars().all():
                category.is_active = False
            await session.commit()


# ---------- Weight categories ----------

async def get_active_weight_categories(vehicle_id: int) -> list[WeightCategory]:
    async with async_session() as session:
        result = await session.execute(
            select(WeightCategory)
            .where(WeightCategory.vehicle_type_id == vehicle_id, WeightCategory.is_active.is_(True))
            .order_by(WeightCategory.sort_order, WeightCategory.id)
        )
        return list(result.scalars().all())


async def get_all_weight_categories(vehicle_id: int) -> list[WeightCategory]:
    async with async_session() as session:
        result = await session.execute(
            select(WeightCategory)
            .where(WeightCategory.vehicle_type_id == vehicle_id)
            .order_by(WeightCategory.sort_order, WeightCategory.id)
        )
        return list(result.scalars().all())


async def get_weight_category_by_id(category_id: int) -> WeightCategory | None:
    async with async_session() as session:
        result = await session.execute(
            select(WeightCategory)
            .options(selectinload(WeightCategory.vehicle_type))
            .where(WeightCategory.id == category_id)
        )
        return result.scalar_one_or_none()


async def create_weight_category(
    vehicle_id: int, label: str, city_price: int, price_per_km: int
) -> WeightCategory:
    async with async_session() as session:
        result = await session.execute(
            select(func.max(WeightCategory.sort_order)).where(
                WeightCategory.vehicle_type_id == vehicle_id
            )
        )
        max_order = result.scalar() or 0
        category = WeightCategory(
            vehicle_type_id=vehicle_id,
            label=label,
            city_price=city_price,
            price_per_km=price_per_km,
            is_active=True,
            sort_order=max_order + 1,
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


async def update_weight_category_price(
    category_id: int, city_price: int | None = None, price_per_km: int | None = None
) -> None:
    async with async_session() as session:
        category = await session.get(WeightCategory, category_id)
        if category:
            if city_price is not None:
                category.city_price = city_price
            if price_per_km is not None:
                category.price_per_km = price_per_km
            await session.commit()


async def rename_weight_category(category_id: int, new_label: str) -> None:
    async with async_session() as session:
        category = await session.get(WeightCategory, category_id)
        if category:
            category.label = new_label
            await session.commit()


async def deactivate_weight_category(category_id: int) -> None:
    async with async_session() as session:
        category = await session.get(WeightCategory, category_id)
        if category:
            category.is_active = False
            await session.commit()


# ---------- Requests ----------

async def create_request(
    user_id: int,
    username: str | None,
    full_name: str | None,
    vehicle_type: str,
    weight_category: str,
    trip_type: str,
    km: int | None,
    calculated_price: int,
) -> Request:
    async with async_session() as session:
        request = Request(
            user_id=user_id,
            username=username,
            full_name=full_name,
            vehicle_type=vehicle_type,
            weight_category=weight_category,
            trip_type=trip_type,
            km=km,
            calculated_price=calculated_price,
        )
        session.add(request)
        await session.commit()
        await session.refresh(request)
        return request


async def get_recent_requests(limit: int = 20, offset: int = 0) -> list[Request]:
    async with async_session() as session:
        result = await session.execute(
            select(Request)
            .order_by(Request.created_at.desc(), Request.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())


async def count_requests_total() -> int:
    async with async_session() as session:
        result = await session.execute(select(func.count(Request.id)))
        return result.scalar_one()


async def count_requests_since(since: datetime) -> int:
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Request.id)).where(Request.created_at >= since)
        )
        return result.scalar_one()


async def count_requests_by_category() -> list[tuple[str, str, int]]:
    async with async_session() as session:
        result = await session.execute(
            select(Request.vehicle_type, Request.weight_category, func.count(Request.id))
            .group_by(Request.vehicle_type, Request.weight_category)
            .order_by(func.count(Request.id).desc())
        )
        return [tuple(row) for row in result.all()]
