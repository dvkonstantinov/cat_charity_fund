from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationDB, DonationCreate
from app.services.investing import investing_process

EXCLUDE_FIELDS = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)

router = APIRouter()


@router.get('/',
            response_model=List[DonationDB],
            dependencies=[Depends(current_superuser)],
            response_model_exclude_none=True)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post('/',
             response_model=DonationDB,
             response_model_exclude={*EXCLUDE_FIELDS},
             response_model_exclude_none=True)
async def create_donation(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation_in, session)
    await investing_process(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get('/my',
            response_model=List[DonationDB],
            response_model_exclude={*EXCLUDE_FIELDS}
            )
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Get all the donations for the current user."""
    donations = await donation_crud.get_donations_by_user(
        session=session, user=user
    )
    return donations
