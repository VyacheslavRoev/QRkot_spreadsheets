from datetime import datetime
from typing import List, Type, TypeVar, Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation


ModelType = TypeVar('ModelType', CharityProject, Donation)


async def close_project_donation(
    obj: Union[CharityProject, Donation]
) -> None:
    """Закрыть проект или пожертвование."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def get_all_open(
    model: Type[ModelType],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    """Получить все открытые проекты или пожертвования."""
    open_objects = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(model.create_date)
    )
    open_objects = open_objects.scalars().all()
    return open_objects


async def investing_for_project(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Распределить пожертвования по открытым проектам."""
    model = CharityProject if (isinstance(obj, Donation)) else Donation
    open_objects = await get_all_open(model, session)
    if open_objects:
        amount_invest = obj.full_amount
        for object in open_objects:
            amount = object.full_amount - object.invested_amount
            invest_amount = min(amount, amount_invest)
            object.invested_amount += invest_amount
            obj.invested_amount += invest_amount
            amount_invest -= invest_amount

            if object.full_amount == object.invested_amount:
                await close_project_donation(object)

            if not amount_invest:
                await close_project_donation(obj)
                break
        await session.commit()
    return obj