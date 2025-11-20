from typing import Sequence, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session
from app.database.models.requests import Request


async def list_requests(session: AsyncSession, limit: int = 20) -> Sequence[Request]:
    stmt = (
        select(Request)
        .order_by(Request.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_request(
    user_id: int,
    username: Optional[str],
    data: Dict[str, Any],
) -> Request:

    async with async_session() as session:
        title = data.get("title")
        description = data.get("description")
        contact = data.get("contact")
        meta = data.get("meta")

        request_obj = Request(
            user_id=user_id,
            username=username,
            title=title,
            description=description,
            contact=contact,
            meta=meta,
        )

        try:
            session.add(request_obj)
            await session.commit()
            await session.refresh(request_obj)
            return request_obj

        except Exception:
            await session.rollback()
            raise
