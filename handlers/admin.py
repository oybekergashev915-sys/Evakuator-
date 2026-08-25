import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import config
from db.queries import (
    count_requests_by_category,
    count_requests_since,
    count_requests_total,
    create_vehicle_type,
    create_weight_category,
    deactivate_vehicle_type,
    deactivate_weight_category,
    get_all_vehicle_types,
    get_all_weight_categories,
    get_recent_requests,
    get_vehicle_type_by_id,
    get_weight_category_by_id,
    rename_vehicle_type,
    rename_weight_category,
    update_weight_category_price,
)
from keyboards import (
    admin_categories_keyboard,
    admin_menu_keyboard,
    admin_vehicles_keyboard,
    back_to_menu_keyboard,
    cancel_keyboard,
    confirm_keyboard,
    delete_type_keyboard,
    rename_type_keyboard,
    requests_pagination_keyboard,
)
from utils import format_money, validate_positive_int

logger = logging.getLogger(__name__)

admin_router = Router(name="admin")
admin_router.message.filter(F.from_user.id.in_(config.admin_ids))
admin_router.callback_query.filter(F.from_user.id.in_(config.admin_ids))

admin_fallback_router = Router(name="admin_fallback")

REQUESTS_PAGE_SIZE = 20


class PriceEdit(StatesGroup):
    entering_city_price = State()
    entering_price_per_km = State()


class AddVehicle(StatesGroup):
    entering_name = State()


class AddCategory(StatesGroup):
    entering_label = State()
    entering_city_price = State()
    entering_price_per_km = State()


class RenameVehicle(StatesGroup):
    entering_name = State()


class RenameCategory(StatesGroup):
    entering_label = State()


def _name_ok(text: str) -> bool:
    return bool(text) and 0 < len(text) <= 100


# ---------- Access control / menu ----------

@admin_fallback_router.message(Command("admin"))
async def admin_denied(message: Message):
    await message.answer("⛔ Эта команда доступна только администраторам.")


@admin_router.message(Command("admin"))
async def admin_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠 Панель администратора", reply_markup=admin_menu_keyboard())


@admin_router.callback_query(F.data == "adm:menu")
async def admin_menu_cb(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🛠 Панель администратора", reply_markup=admin_menu_keyboard())
    await callback.answer()


@admin_router.callback_query(F.data == "adm:cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🛠 Панель администратора", reply_markup=admin_menu_keyboard())
    await callback.answer("Отменено")


# ---------- Price list ----------

@admin_router.callback_query(F.data == "adm:price_list")
async def price_list(callback: CallbackQuery):
    vehicles = await get_all_vehicle_types()
    if not vehicles:
        await callback.message.edit_text("Список марок пуст.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return

    lines = ["💰 Текущий прайс:\n"]
    for v in vehicles:
        mark = "" if v.is_active else " (неактивна)"
        lines.append(f"🚛 {v.name}{mark}")
        categories = await get_all_weight_categories(v.id)
        if not categories:
            lines.append("   — нет категорий")
        for c in categories:
            cmark = "" if c.is_active else " (неактивна)"
            lines.append(
                f"   • {c.label}{cmark} — по городу: {format_money(c.city_price)}, "
                f"за городом: {format_money(c.price_per_km)}/км"
            )
        lines.append("")

    await callback.message.edit_text("\n".join(lines), reply_markup=back_to_menu_keyboard())
    await callback.answer()


# ---------- Price edit ----------

@admin_router.callback_query(F.data == "adm:price_edit")
async def price_edit_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    vehicles = await get_all_vehicle_types()
    if not vehicles:
        await callback.message.edit_text("Список марок пуст.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку эвакуатора:", reply_markup=admin_vehicles_keyboard(vehicles, "adm:pe:vehicle")
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:pe:vehicle:"))
async def price_edit_choose_vehicle(callback: CallbackQuery):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    categories = await get_all_weight_categories(vehicle_id)
    if not categories:
        await callback.message.edit_text("У этой марки нет категорий.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите весовую категорию:",
        reply_markup=admin_categories_keyboard(categories, "adm:pe:category"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:pe:category:"))
async def price_edit_choose_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.rsplit(":", 1)[-1])
    category = await get_weight_category_by_id(category_id)
    if not category:
        await callback.answer("Категория не найдена.", show_alert=True)
        return
    await state.update_data(category_id=category_id)
    await state.set_state(PriceEdit.entering_city_price)
    await callback.message.edit_text(
        f"Категория: {category.label}\n"
        f"Текущая цена по городу: {format_money(category.city_price)}\n\n"
        "Введите новую цену по городу (целое число, сум) или «-», чтобы оставить без изменений:",
        reply_markup=cancel_keyboard(),
    )
    await callback.answer()


@admin_router.message(PriceEdit.entering_city_price)
async def price_edit_city_price(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if text == "-":
        city_price = None
    else:
        try:
            city_price = validate_positive_int(text, "цена по городу")
        except ValueError as e:
            await message.answer(f"⚠️ {e}", reply_markup=cancel_keyboard())
            return

    await state.update_data(new_city_price=city_price)
    data = await state.get_data()
    category = await get_weight_category_by_id(data["category_id"])
    await state.set_state(PriceEdit.entering_price_per_km)
    await message.answer(
        f"Текущий тариф за городом: {format_money(category.price_per_km)}/км\n\n"
        "Введите новый тариф за км за городом (целое число, сум) или «-», чтобы оставить без изменений:",
        reply_markup=cancel_keyboard(),
    )


@admin_router.message(PriceEdit.entering_price_per_km)
async def price_edit_per_km(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if text == "-":
        price_per_km = None
    else:
        try:
            price_per_km = validate_positive_int(text, "тариф за км")
        except ValueError as e:
            await message.answer(f"⚠️ {e}", reply_markup=cancel_keyboard())
            return

    data = await state.get_data()
    category_id = data["category_id"]
    new_city_price = data.get("new_city_price")

    await update_weight_category_price(category_id, city_price=new_city_price, price_per_km=price_per_km)
    category = await get_weight_category_by_id(category_id)
    await state.clear()
    await message.answer(
        f"✅ Цены обновлены для «{category.label}»:\n"
        f"По городу: {format_money(category.city_price)}\n"
        f"За городом: {format_money(category.price_per_km)}/км",
        reply_markup=back_to_menu_keyboard(),
    )


# ---------- Add vehicle ----------

@admin_router.callback_query(F.data == "adm:add_vehicle")
async def add_vehicle_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddVehicle.entering_name)
    await callback.message.edit_text(
        "Введите название новой марки эвакуатора:", reply_markup=cancel_keyboard()
    )
    await callback.answer()


@admin_router.message(AddVehicle.entering_name)
async def add_vehicle_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if not _name_ok(name):
        await message.answer(
            "⚠️ Название должно быть от 1 до 100 символов. Попробуйте ещё раз:",
            reply_markup=cancel_keyboard(),
        )
        return
    vehicle = await create_vehicle_type(name)
    await state.clear()
    await message.answer(f"✅ Марка «{vehicle.name}» добавлена.", reply_markup=back_to_menu_keyboard())


# ---------- Add category ----------

@admin_router.callback_query(F.data == "adm:add_category")
async def add_category_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    vehicles = await get_all_vehicle_types()
    if not vehicles:
        await callback.message.edit_text(
            "Сначала добавьте марку эвакуатора.", reply_markup=back_to_menu_keyboard()
        )
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку, для которой добавляется категория:",
        reply_markup=admin_vehicles_keyboard(vehicles, "adm:ac:vehicle"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:ac:vehicle:"))
async def add_category_choose_vehicle(callback: CallbackQuery, state: FSMContext):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    await state.update_data(vehicle_id=vehicle_id)
    await state.set_state(AddCategory.entering_label)
    await callback.message.edit_text(
        "Введите название весовой категории (например: до 5 тонн):",
        reply_markup=cancel_keyboard(),
    )
    await callback.answer()


@admin_router.message(AddCategory.entering_label)
async def add_category_label(message: Message, state: FSMContext):
    label = (message.text or "").strip()
    if not _name_ok(label):
        await message.answer(
            "⚠️ Название должно быть от 1 до 100 символов. Попробуйте ещё раз:",
            reply_markup=cancel_keyboard(),
        )
        return
    await state.update_data(label=label)
    await state.set_state(AddCategory.entering_city_price)
    await message.answer("Введите цену по городу (целое число, сум):", reply_markup=cancel_keyboard())


@admin_router.message(AddCategory.entering_city_price)
async def add_category_city_price(message: Message, state: FSMContext):
    try:
        city_price = validate_positive_int(message.text or "", "цена по городу")
    except ValueError as e:
        await message.answer(f"⚠️ {e}", reply_markup=cancel_keyboard())
        return
    await state.update_data(city_price=city_price)
    await state.set_state(AddCategory.entering_price_per_km)
    await message.answer(
        "Введите тариф за км за пределами города (целое число, сум):", reply_markup=cancel_keyboard()
    )


@admin_router.message(AddCategory.entering_price_per_km)
async def add_category_per_km(message: Message, state: FSMContext):
    try:
        price_per_km = validate_positive_int(message.text or "", "тариф за км")
    except ValueError as e:
        await message.answer(f"⚠️ {e}", reply_markup=cancel_keyboard())
        return

    data = await state.get_data()
    category = await create_weight_category(
        vehicle_id=data["vehicle_id"],
        label=data["label"],
        city_price=data["city_price"],
        price_per_km=price_per_km,
    )
    await state.clear()
    await message.answer(
        f"✅ Категория «{category.label}» добавлена:\n"
        f"По городу: {format_money(category.city_price)}\n"
        f"За городом: {format_money(category.price_per_km)}/км",
        reply_markup=back_to_menu_keyboard(),
    )


# ---------- Rename ----------

@admin_router.callback_query(F.data == "adm:rename_menu")
async def rename_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Что переименовать?", reply_markup=rename_type_keyboard())
    await callback.answer()


@admin_router.callback_query(F.data == "adm:ren:type:vehicle")
async def rename_pick_vehicle_type(callback: CallbackQuery):
    vehicles = await get_all_vehicle_types()
    if not vehicles:
        await callback.message.edit_text("Список марок пуст.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку для переименования:",
        reply_markup=admin_vehicles_keyboard(vehicles, "adm:ren:vehicle"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:ren:vehicle:"))
async def rename_vehicle_start(callback: CallbackQuery, state: FSMContext):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    await state.update_data(vehicle_id=vehicle_id)
    await state.set_state(RenameVehicle.entering_name)
    await callback.message.edit_text("Введите новое название марки:", reply_markup=cancel_keyboard())
    await callback.answer()


@admin_router.message(RenameVehicle.entering_name)
async def rename_vehicle_apply(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if not _name_ok(name):
        await message.answer(
            "⚠️ Название должно быть от 1 до 100 символов. Попробуйте ещё раз:",
            reply_markup=cancel_keyboard(),
        )
        return
    data = await state.get_data()
    await rename_vehicle_type(data["vehicle_id"], name)
    await state.clear()
    await message.answer(f"✅ Марка переименована в «{name}».", reply_markup=back_to_menu_keyboard())


@admin_router.callback_query(F.data == "adm:ren:type:category")
async def rename_pick_category_vehicle(callback: CallbackQuery):
    vehicles = await get_all_vehicle_types()
    if not vehicles:
        await callback.message.edit_text("Список марок пуст.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку:", reply_markup=admin_vehicles_keyboard(vehicles, "adm:ren:catvehicle")
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:ren:catvehicle:"))
async def rename_pick_category(callback: CallbackQuery):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    categories = await get_all_weight_categories(vehicle_id)
    if not categories:
        await callback.message.edit_text("У этой марки нет категорий.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите категорию для переименования:",
        reply_markup=admin_categories_keyboard(categories, "adm:ren:category"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:ren:category:"))
async def rename_category_start(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.rsplit(":", 1)[-1])
    await state.update_data(category_id=category_id)
    await state.set_state(RenameCategory.entering_label)
    await callback.message.edit_text("Введите новое название категории:", reply_markup=cancel_keyboard())
    await callback.answer()


@admin_router.message(RenameCategory.entering_label)
async def rename_category_apply(message: Message, state: FSMContext):
    label = (message.text or "").strip()
    if not _name_ok(label):
        await message.answer(
            "⚠️ Название должно быть от 1 до 100 символов. Попробуйте ещё раз:",
            reply_markup=cancel_keyboard(),
        )
        return
    data = await state.get_data()
    await rename_weight_category(data["category_id"], label)
    await state.clear()
    await message.answer(f"✅ Категория переименована в «{label}».", reply_markup=back_to_menu_keyboard())


# ---------- Delete / deactivate ----------

@admin_router.callback_query(F.data == "adm:delete_menu")
async def delete_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Что вы хотите удалить (деактивировать)?", reply_markup=delete_type_keyboard()
    )
    await callback.answer()


@admin_router.callback_query(F.data == "adm:del:type:vehicle")
async def delete_pick_vehicle(callback: CallbackQuery):
    vehicles = [v for v in await get_all_vehicle_types() if v.is_active]
    if not vehicles:
        await callback.message.edit_text("Нет активных марок для удаления.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку для деактивации:",
        reply_markup=admin_vehicles_keyboard(vehicles, "adm:del:vehicle"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:del:vehicle:"))
async def delete_vehicle_confirm(callback: CallbackQuery):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    vehicle = await get_vehicle_type_by_id(vehicle_id)
    if not vehicle:
        await callback.answer("Марка не найдена.", show_alert=True)
        return
    await callback.message.edit_text(
        f"Вы уверены, что хотите деактивировать марку «{vehicle.name}»?\n"
        "Все её категории тоже станут неактивны. История заявок сохранится.",
        reply_markup=confirm_keyboard(f"adm:del:vehicledo:{vehicle_id}"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:del:vehicledo:"))
async def delete_vehicle_apply(callback: CallbackQuery):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    await deactivate_vehicle_type(vehicle_id)
    await callback.message.edit_text("✅ Марка деактивирована.", reply_markup=back_to_menu_keyboard())
    await callback.answer()


@admin_router.callback_query(F.data == "adm:del:type:category")
async def delete_pick_category_vehicle(callback: CallbackQuery):
    vehicles = [v for v in await get_all_vehicle_types() if v.is_active]
    if not vehicles:
        await callback.message.edit_text("Нет активных марок.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите марку:", reply_markup=admin_vehicles_keyboard(vehicles, "adm:del:catvehicle")
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:del:catvehicle:"))
async def delete_pick_category(callback: CallbackQuery):
    vehicle_id = int(callback.data.rsplit(":", 1)[-1])
    categories = [c for c in await get_all_weight_categories(vehicle_id) if c.is_active]
    if not categories:
        await callback.message.edit_text(
            "У этой марки нет активных категорий.", reply_markup=back_to_menu_keyboard()
        )
        await callback.answer()
        return
    await callback.message.edit_text(
        "Выберите категорию для деактивации:",
        reply_markup=admin_categories_keyboard(categories, "adm:del:category"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:del:category:"))
async def delete_category_confirm(callback: CallbackQuery):
    category_id = int(callback.data.rsplit(":", 1)[-1])
    category = await get_weight_category_by_id(category_id)
    if not category:
        await callback.answer("Категория не найдена.", show_alert=True)
        return
    await callback.message.edit_text(
        f"Вы уверены, что хотите деактивировать категорию «{category.label}»?",
        reply_markup=confirm_keyboard(f"adm:del:categorydo:{category_id}"),
    )
    await callback.answer()


@admin_router.callback_query(F.data.startswith("adm:del:categorydo:"))
async def delete_category_apply(callback: CallbackQuery):
    category_id = int(callback.data.rsplit(":", 1)[-1])
    await deactivate_weight_category(category_id)
    await callback.message.edit_text("✅ Категория деактивирована.", reply_markup=back_to_menu_keyboard())
    await callback.answer()


# ---------- Recent requests ----------

@admin_router.callback_query(F.data.startswith("adm:requests:"))
async def show_requests(callback: CallbackQuery):
    page = int(callback.data.rsplit(":", 1)[-1])
    offset = page * REQUESTS_PAGE_SIZE
    requests_list = await get_recent_requests(limit=REQUESTS_PAGE_SIZE + 1, offset=offset)
    has_next = len(requests_list) > REQUESTS_PAGE_SIZE
    requests_list = requests_list[:REQUESTS_PAGE_SIZE]

    if not requests_list and page == 0:
        await callback.message.edit_text("Заявок пока нет.", reply_markup=back_to_menu_keyboard())
        await callback.answer()
        return
    if not requests_list:
        await callback.answer("Больше заявок нет.", show_alert=True)
        return

    lines = [f"📋 Заявки (страница {page + 1}):\n"]
    for r in requests_list:
        who = f"@{r.username}" if r.username else (r.full_name or f"id{r.user_id}")
        when = r.created_at.strftime("%d.%m.%Y %H:%M")
        km_part = f", {r.km} км" if r.km is not None else ""
        lines.append(
            f"🕐 {when} — {who}\n"
            f"   {r.vehicle_type}, {r.weight_category}, {r.trip_type}{km_part} — {format_money(r.calculated_price)}"
        )

    await callback.message.edit_text(
        "\n".join(lines), reply_markup=requests_pagination_keyboard(page, has_next)
    )
    await callback.answer()


# ---------- Stats ----------

@admin_router.callback_query(F.data == "adm:stats")
async def show_stats(callback: CallbackQuery):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    week_ago = now - timedelta(days=7)

    total = await count_requests_total()
    today = await count_requests_since(today_start)
    week = await count_requests_since(week_ago)
    by_category = await count_requests_by_category()

    lines = [
        "📊 Статистика заявок:\n",
        f"За сегодня: {today}",
        f"За 7 дней: {week}",
        f"За всё время: {total}",
        "",
        "По категориям:",
    ]
    if by_category:
        for vehicle_type, weight_category, count in by_category:
            lines.append(f"   • {vehicle_type} / {weight_category}: {count}")
    else:
        lines.append("   — пока нет данных")

    await callback.message.edit_text("\n".join(lines), reply_markup=back_to_menu_keyboard())
    await callback.answer()
