from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config


# ---------- Client keyboards ----------

def start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🧮 Рассчитать стоимость", callback_data="calc:start")
    builder.adjust(1)
    return builder.as_markup()


def vehicle_types_keyboard(vehicles) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for v in vehicles:
        builder.button(text=v.name, callback_data=f"calc:vehicle:{v.id}")
    builder.adjust(1)
    return builder.as_markup()


def weight_categories_keyboard(categories) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for c in categories:
        builder.button(text=c.label, callback_data=f"calc:cat:{c.id}")
    builder.button(text="⬅️ Назад к маркам", callback_data="calc:back_vehicles")
    builder.adjust(1)
    return builder.as_markup()


def trip_type_keyboard(category_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏙 По городу Ташкент", callback_data=f"calc:trip:city:{category_id}")
    builder.button(text="🛣 За пределами города", callback_data=f"calc:trip:out:{category_id}")
    builder.adjust(1)
    return builder.as_markup()


def _contact_url() -> str:
    contact = config.admin_contact.strip()
    if contact.startswith("@"):
        return f"https://t.me/{contact[1:]}"
    digits_only = contact.replace(" ", "").replace("+", "")
    if contact.startswith("+") or digits_only.isdigit():
        digits = "".join(ch for ch in contact if ch.isdigit() or ch == "+")
        return f"tel:{digits}"
    return f"https://t.me/{contact}"


def contact_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Связаться с водителем", url=_contact_url())
    builder.adjust(1)
    return builder.as_markup()


def after_result_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📞 Связаться с водителем", url=_contact_url())
    builder.button(text="🔄 Новый расчёт", callback_data="calc:new")
    builder.adjust(1)
    return builder.as_markup()


# ---------- Admin keyboards ----------

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 Текущий прайс", callback_data="adm:price_list")
    builder.button(text="✏️ Изменить цену", callback_data="adm:price_edit")
    builder.button(text="➕ Добавить марку", callback_data="adm:add_vehicle")
    builder.button(text="➕ Добавить категорию", callback_data="adm:add_category")
    builder.button(text="🗑 Удалить/деактивировать", callback_data="adm:delete_menu")
    builder.button(text="✍️ Переименовать", callback_data="adm:rename_menu")
    builder.button(text="📋 Последние заявки", callback_data="adm:requests:0")
    builder.button(text="📊 Статистика", callback_data="adm:stats")
    builder.adjust(1)
    return builder.as_markup()


def cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="adm:cancel")
    builder.adjust(1)
    return builder.as_markup()


def admin_vehicles_keyboard(vehicles, prefix: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for v in vehicles:
        text = v.name if v.is_active else f"{v.name} (неактивна)"
        builder.button(text=text, callback_data=f"{prefix}:{v.id}")
    builder.button(text="❌ Отмена", callback_data="adm:cancel")
    builder.adjust(1)
    return builder.as_markup()


def admin_categories_keyboard(categories, prefix: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for c in categories:
        text = c.label if c.is_active else f"{c.label} (неактивна)"
        builder.button(text=text, callback_data=f"{prefix}:{c.id}")
    builder.button(text="❌ Отмена", callback_data="adm:cancel")
    builder.adjust(1)
    return builder.as_markup()


def confirm_keyboard(yes_data: str, no_data: str = "adm:cancel") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data=yes_data)
    builder.button(text="❌ Нет", callback_data=no_data)
    builder.adjust(2)
    return builder.as_markup()


def requests_pagination_keyboard(page: int, has_next: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"adm:requests:{page - 1}")
    if has_next:
        builder.button(text="➡️ Далее", callback_data=f"adm:requests:{page + 1}")
    builder.button(text="🏠 В меню", callback_data="adm:menu")
    builder.adjust(2, 1)
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 В меню", callback_data="adm:menu")
    builder.adjust(1)
    return builder.as_markup()


def delete_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Марку эвакуатора", callback_data="adm:del:type:vehicle")
    builder.button(text="Весовую категорию", callback_data="adm:del:type:category")
    builder.button(text="❌ Отмена", callback_data="adm:cancel")
    builder.adjust(1)
    return builder.as_markup()


def rename_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Марку эвакуатора", callback_data="adm:ren:type:vehicle")
    builder.button(text="Весовую категорию", callback_data="adm:ren:type:category")
    builder.button(text="❌ Отмена", callback_data="adm:cancel")
    builder.adjust(1)
    return builder.as_markup()
