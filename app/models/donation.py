from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import ProjectBaseModel


class Donation(ProjectBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
