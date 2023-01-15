from datetime import datetime
from typing import Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.donation import Donation
from app.models.charity_project import CharityProject


async def get_not_invested_objects(
        model_in: Union[CharityProject, Donation],
        session: AsyncSession
) -> List[Union[CharityProject, Donation]]:

    objects = await session.execute(select(model_in).where(
        model_in.fully_invested == false()).order_by(model_in.create_date))
    objects = objects.scalars().all()
    return objects


async def investing_process(
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession
):
    if isinstance(obj_in, Donation):
        model_db = CharityProject
    else:
        model_db = Donation
    not_invested_projects = await get_not_invested_objects(
        model_db, session
    )
    available_amount = obj_in.full_amount
    if not_invested_projects:
        for object in not_invested_projects:
            needs_invest = (object.full_amount -
                            object.invested_amount)
            if needs_invest < available_amount:
                current_investing = needs_invest
            else:
                current_investing = available_amount
            object.invested_amount += current_investing
            obj_in.invested_amount += current_investing
            available_amount -= current_investing

            if object.full_amount == object.invested_amount:
                object.fully_invested = True
                object.close_date = datetime.now()

            if not available_amount:
                obj_in.fully_invested = True
                obj_in.close_date = datetime.now()
        await session.commit()
    return obj_in
