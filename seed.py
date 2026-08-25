import asyncio

from sqlalchemy import select

from db.models import VehicleType, WeightCategory, async_session, init_models

SEED_DATA = [
    ("Газель", [
        ("до 2 тонн", 350000, 10000),
        ("до 2.7 тонн", 400000, 13000),
    ]),
    ("Исузу", [
        ("до 3.5 тонн", 500000, 17000),
        ("до 7.0 тонн", 700000, 20000),
    ]),
]


async def seed() -> None:
    await init_models()
    async with async_session() as session:
        result = await session.execute(select(VehicleType))
        if result.scalars().first():
            print("База уже содержит данные, засев пропущен.")
            return

        for vehicle_name, categories in SEED_DATA:
            vehicle = VehicleType(name=vehicle_name, is_active=True)
            session.add(vehicle)
            await session.flush()
            for order, (label, city_price, price_per_km) in enumerate(categories):
                session.add(
                    WeightCategory(
                        vehicle_type_id=vehicle.id,
                        label=label,
                        city_price=city_price,
                        price_per_km=price_per_km,
                        is_active=True,
                        sort_order=order,
                    )
                )
        await session.commit()
        print("База данных успешно засеяна начальными данными.")


if __name__ == "__main__":
    asyncio.run(seed())
