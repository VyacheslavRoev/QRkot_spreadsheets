from sqlalchemy import Column, String, Text

from .base import ProjectBaseModel


class CharityProject(ProjectBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
