import datetime as dt

from sqlalchemy import func, select

from app.db.engine import async_session
from app.db.models import Lead


async def add_lead(user_id: int, username: str | None, name: str, phone: str, description: str) -> Lead:
    async with async_session() as session:
        lead = Lead(
            user_id=user_id,
            username=username,
            name=name,
            phone=phone,
            description=description,
        )
        session.add(lead)
        await session.commit()
        await session.refresh(lead)
        return lead


async def get_last_leads(limit: int = 10) -> list[Lead]:
    async with async_session() as session:
        result = await session.execute(
            select(Lead).order_by(Lead.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())


async def get_stats() -> tuple[int, int]:
    today_start = dt.datetime.combine(dt.date.today(), dt.time.min)
    async with async_session() as session:
        total = await session.scalar(select(func.count(Lead.id)))
        today = await session.scalar(
            select(func.count(Lead.id)).where(Lead.created_at >= today_start)
        )
        return today or 0, total or 0
