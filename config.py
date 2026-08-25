import os

from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _parse_admin_ids(raw: str) -> list[int]:
    ids = []
    for part in raw.split(","):
        part = part.strip()
        if part:
            ids.append(int(part))
    return ids


@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]
    admin_contact: str
    db_path: str = "evacuator.db"


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "")
    admin_ids_raw = os.getenv("ADMIN_IDS", "")
    admin_contact = os.getenv("ADMIN_CONTACT", "")
    db_path = os.getenv("DB_PATH", "evacuator.db")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN не задан в .env")
    if not admin_ids_raw:
        raise RuntimeError("ADMIN_IDS не задан в .env")
    if not admin_contact:
        raise RuntimeError("ADMIN_CONTACT не задан в .env")

    return Config(
        bot_token=bot_token,
        admin_ids=_parse_admin_ids(admin_ids_raw),
        admin_contact=admin_contact,
        db_path=db_path,
    )


config = load_config()
