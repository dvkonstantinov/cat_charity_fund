from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra

EXAMPLE_DATETIME = (datetime.now() - timedelta(minutes=10)).isoformat(
    timespec='seconds')


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectFull(CharityProjectBase):
    pass


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime = Field(..., example=EXAMPLE_DATETIME)
    close_date: Optional[datetime] = Field(None, example=EXAMPLE_DATETIME)

    class Config:
        orm_mode = True
