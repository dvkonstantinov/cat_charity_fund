from sqlalchemy import Column, Integer, ForeignKey, Text

from app.core.db import BaseDonationCharity


class Donation(BaseDonationCharity):
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name='fk_donation_user_id_user'
    ))
    comment = Column(Text)
