from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate


class CRUDCharity(CRUDBase):

    async def get_charity_project(
            self,
            object_id: int,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        project_db = await session.execute(
            select(CharityProject).where(
                CharityProject.id == object_id
            )
        )
        return project_db.scalars().first()

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project.scalars().first()

    async def remove(
            self,
            project: CharityProject,
            session: AsyncSession
    ):
        await session.delete(project)
        await session.commit()
        return project

    async def update(
            self,
            db_obj: CharityProject,
            obj_in: CharityProjectCreate,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


charity_crud = CRUDCharity(CharityProject)
