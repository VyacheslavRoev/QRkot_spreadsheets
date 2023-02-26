from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import AllDonationsDB, DonationCreate, DonationDB
from app.services.investing import investing_for_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Посмотреть все пожертвования. Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование. Для авторизованных."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing_for_project(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Cписок всех пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(session, user)
    return donations