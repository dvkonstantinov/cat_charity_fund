from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_project_exist, check_project_was_donated,
    check_project_was_closed, check_correct_new_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.investing import investing_process

router = APIRouter()


@router.get('/',
            response_model=List[CharityProjectDB],
            response_model_exclude_none=True
            )
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_crud.get_multi(session)
    return all_projects


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)],
             response_model_exclude_none=True
             )
async def create_new_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_crud.create(project, session)

    await investing_process(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exist(project_id, session)
    check_project_was_donated(project)
    await charity_crud.remove(project, session)
    return project


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exist(project_id, session)
    check_project_was_closed(project)

    if obj_in.full_amount:
        check_correct_new_amount(project, obj_in.full_amount)

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    project = await charity_crud.update(project, obj_in, session)
    return project
