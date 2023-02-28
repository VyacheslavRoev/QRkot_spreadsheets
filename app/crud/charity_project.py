import logging
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def update_charityproject(
        self,
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_project)
        update_data = project_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_project, field, update_data[field])
        try:
            session.add(db_project)
        except Exception:
            session.rollback()
            logging.error('Не получилось записать данные в базу!', exc_info=True, stack_info=True)
        else:
            await session.commit()
            await session.refresh(db_project)
        return db_project

    async def delete_charityproject(
        self,
        db_project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_project)
        await session.commit()
        return db_project

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ):
        completed_projects = await session.execute(
            select(CharityProject.name,
                   CharityProject.description,
                   CharityProject.close_date,
                   CharityProject.create_date).where(CharityProject.fully_invested))
        completed_projects = completed_projects.all()
        result = []
        for project in completed_projects:
            result.append({
                'name': project.name,
                'time_delta': (project.close_date - project.create_date),
                'description': project.description
            })
        result_sorted = sorted(result, key=lambda x: x['time_delta'])
        return result_sorted


charity_project_crud = CRUDCharityProject(CharityProject)
