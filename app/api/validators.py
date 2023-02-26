from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services.investing import close_project_donation


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка названия проекта на уникальность."""
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка, что проект существует."""
    charity_project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_closed(
    project: CharityProject,
) -> None:
    """Проверка, закрыт ли проект"""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_to_invested_amount(
    project_id: int,
    full_amount: PositiveInt,
    session: AsyncSession,
) -> None:
    """Проверка изменения требуемой суммы."""
    charity_project = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма не может быть меньше внесённой!'
        )
    if full_amount == charity_project.invested_amount:
        await close_project_donation(charity_project)


async def check_project_investing(
    project: CharityProject
) -> None:
    """Проверка, что в проект уже внесены средства."""
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
