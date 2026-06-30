from aiogram import Router
from aiogram.filters import Command

from app.db.requests import get_last_leads, get_stats
from app.filters.admin import IsAdmin

router = Router()
router.message.filter(IsAdmin())


@router.message(Command("admin"))
async def cmd_admin(message) -> None:
    leads = await get_last_leads(10)
    if not leads:
        await message.answer("Заявок пока нет.")
        return

    lines = ["📋 Последние заявки:\n"]
    for lead in leads:
        lines.append(
            f"#{lead.id} | {lead.created_at:%d.%m.%Y %H:%M}\n"
            f"👤 {lead.name} | 📱 {lead.phone}\n"
            f"💬 {lead.description}\n"
        )
    await message.answer("\n".join(lines))


@router.message(Command("stats"))
async def cmd_stats(message) -> None:
    today, total = await get_stats()
    await message.answer(
        f"📊 Статистика заявок\n\nСегодня: {today}\nВсего: {total}"
    )
