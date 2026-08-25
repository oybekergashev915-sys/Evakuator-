import logging
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import config
from db.queries import (
    create_request,
    get_active_vehicle_types,
    get_active_weight_categories,
    get_vehicle_type_by_id,
    get_weight_category_by_id,
)
from keyboards import (
    after_result_keyboard,
    contact_keyboard,
    start_keyboard,
    trip_type_keyboard,
    vehicle_types_keyboard,
    weight_categories_keyboard,
)
from utils import calculate_price, format_km, format_money, validate_km

logger = logging.getLogger(__name__)

router = Router(name="client")

MAX_KM = 3000


class ClientFlow(StatesGroup):
    entering_km = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Здравствуйте! Это бот-калькулятор стоимости эвакуатора в Ташкенте.\n\n"
        "Нажмите кнопку ниже, чтобы рассчитать стоимость.",
        reply_markup=start_keyboard(),
    )


@router.callback_query(F.data == "calc:start")
async def calc_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_vehicle_types(callback)


@router.callback_query(F.data == "calc:new")
async def calc_new(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await show_vehicle_types(callback)


async def show_vehicle_types(callback: CallbackQuery):
    vehicles = await get_active_vehicle_types()
    if not vehicles:
        await callback.message.edit_text(
            "😔 К сожалению, расчёт временно недоступен. Свяжитесь с нами напрямую.",
            reply_markup=contact_keyboard(),
        )
        await callback.answer()
        return
    await callback.message.edit_text(
        "🚛 Выберите марку эвакуатора:",
        reply_markup=vehicle_types_keyboard(vehicles),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("calc:vehicle:"))
async def choose_vehicle(callback: CallbackQuery, state: FSMContext):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    vehicle = await get_vehicle_type_by_id(vehicle_id)
    if not vehicle or not vehicle.is_active:
        await callback.answer("Эта марка больше недоступна, выберите другую.", show_alert=True)
        await show_vehicle_types(callback)
        return

    categories = await get_active_weight_categories(vehicle_id)
    if not categories:
        await callback.message.edit_text(
            "😔 Для этой марки пока нет доступных категорий. Свяжитесь с нами напрямую.",
            reply_markup=contact_keyboard(),
        )
        await callback.answer()
        return

    await state.update_data(vehicle_id=vehicle_id, vehicle_name=vehicle.name)
    await callback.message.edit_text(
        f"🚛 Марка: {vehicle.name}\n\nВыберите весовую категорию:",
        reply_markup=weight_categories_keyboard(categories),
    )
    await callback.answer()


@router.callback_query(F.data == "calc:back_vehicles")
async def back_to_vehicles(callback: CallbackQuery):
    await show_vehicle_types(callback)


@router.callback_query(F.data.startswith("calc:cat:"))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.rsplit(":", 1)[-1])
    category = await get_weight_category_by_id(category_id)
    if not category or not category.is_active:
        await callback.answer("Эта категория больше недоступна.", show_alert=True)
        return

    data = await state.get_data()
    vehicle_name = data.get("vehicle_name") or category.vehicle_type.name

    await state.update_data(
        vehicle_name=vehicle_name,
        category_id=category_id,
        category_label=category.label,
        city_price=category.city_price,
        price_per_km=category.price_per_km,
    )
    await callback.message.edit_text(
        f"🚛 Марка: {vehicle_name}\n"
        f"⚖️ Категория: {category.label}\n\n"
        "Выберите тип поездки:",
        reply_markup=trip_type_keyboard(category_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("calc:trip:city:"))
async def trip_city(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    city_price = data.get("city_price")
    if city_price is None:
        await callback.answer("Начните расчёт заново.", show_alert=True)
        await show_vehicle_types(callback)
        return

    await callback.answer()
    await finalize_request(
        bot, callback.message.chat.id, callback.from_user, state,
        trip_type="по городу", km=None, price=city_price,
    )


@router.callback_query(F.data.startswith("calc:trip:out:"))
async def trip_out(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get("price_per_km") is None:
        await callback.answer("Начните расчёт заново.", show_alert=True)
        await show_vehicle_types(callback)
        return
    await state.set_state(ClientFlow.entering_km)
    await callback.message.edit_text(
        f"{callback.message.text}\n\n"
        "📍 Введите расстояние в километрах (только число, например: 45):"
    )
    await callback.answer()


@router.message(ClientFlow.entering_km)
async def process_km(message: Message, state: FSMContext, bot: Bot):
    try:
        km = validate_km(message.text, max_km=MAX_KM)
    except ValueError as e:
        await message.answer(f"⚠️ {e}\nПопробуйте ещё раз, введите число километров:")
        return

    data = await state.get_data()
    price_per_km = data.get("price_per_km")
    if price_per_km is None:
        await message.answer("Сессия расчёта устарела. Начните заново: /start")
        await state.clear()
        return

    price = calculate_price(km, price_per_km)
    await finalize_request(
        bot, message.chat.id, message.from_user, state,
        trip_type="за город", km=km, price=price,
    )


async def finalize_request(bot: Bot, chat_id: int, user, state: FSMContext, trip_type: str, km, price: int):
    data = await state.get_data()
    vehicle_name = data.get("vehicle_name", "—")
    category_label = data.get("category_label", "—")

    km_line = f"📍 Расстояние: {format_km(km)} км\n" if km is not None else ""
    summary = (
        "✅ Расчёт готов!\n\n"
        f"🚛 Марка: {vehicle_name}\n"
        f"⚖️ Категория: {category_label}\n"
        f"🧭 Тип поездки: {trip_type}\n"
        f"{km_line}"
        f"💰 Стоимость: {format_money(price)}"
    )

    await bot.send_message(chat_id, summary, reply_markup=after_result_keyboard())

    try:
        await create_request(
            user_id=user.id,
            username=user.username,
            full_name=user.full_name,
            vehicle_type=vehicle_name,
            weight_category=category_label,
            trip_type=trip_type,
            km=round(km) if km is not None else None,
            calculated_price=price,
        )
    except Exception:
        logger.exception("Не удалось сохранить заявку в БД")

    await notify_admins(bot, user, vehicle_name, category_label, trip_type, km, price)
    await state.clear()


async def notify_admins(bot: Bot, user, vehicle_name, category_label, trip_type, km, price):
    who = f"@{user.username}" if user.username else (user.full_name or f"id{user.id}")
    km_line = f"📍 Расстояние: {format_km(km)} км\n" if km is not None else ""
    text = (
        "🚛 Новая заявка на эвакуатор!\n\n"
        f"👤 Клиент: {who} (id: {user.id})\n"
        f"🚛 Марка: {vehicle_name}\n"
        f"⚖️ Категория: {category_label}\n"
        f"🧭 Тип поездки: {trip_type}\n"
        f"{km_line}"
        f"💰 Стоимость: {format_money(price)}\n"
        f"🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    for admin_id in config.admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            logger.exception("Не удалось отправить уведомление админу %s", admin_id)
