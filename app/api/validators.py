from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exist(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await charity_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    return project


def check_project_was_donated(project: CharityProject) -> None:
    invested_amount = project.invested_amount
    if invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_project_was_closed(project: CharityProject) -> None:
    close_date = project.close_date
    print(close_date)
    if close_date is not None:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_correct_new_amount(project: CharityProject, new_amount) -> None:
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )
