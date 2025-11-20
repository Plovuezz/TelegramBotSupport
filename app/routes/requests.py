from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.repositories.requests import list_requests
from app.schemas.requests import RequestListScheme

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[RequestListScheme],
)
async def list_orders(
    session: AsyncSession = Depends(get_session),
):
    requests = await list_requests(session=session, limit=50)
    return requests
