import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    admin_ids: tuple[int, ...] = field(
        default_factory=lambda: tuple(
            int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x
        )
    )
    database_url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///leads.db")
    )

    def __post_init__(self) -> None:
        if not self.bot_token:
            raise RuntimeError(
                "BOT_TOKEN is not set. Create a .env file next to main.py "
                "(see .env.example) or export the environment variable."
            )
        if not self.admin_ids:
            raise RuntimeError(
                "ADMIN_IDS is not set. Add comma-separated Telegram user IDs "
                "to .env, e.g. ADMIN_IDS=123456789,987654321"
            )


config = Config()
