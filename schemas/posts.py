from datetime import datetime
from typing import Annotated, Union
from pydantic import BaseModel, ConfigDict, Field, model_validator
from schemas.sections import Section
from schemas.tags import Tag


class PostBase(BaseModel):
    title: Annotated[str, Field(..., max_length=60, min_length=6)]
    body: str
    tags: list[str] = []


class PostCreate(PostBase):
    section_id: int


class PostUpdate(PostBase):
    title: Annotated[Union[str, None], Field(max_length=60)] = None
    body: Union[str, None] = None
    section_id: Union[int, None] = None
    tags: list[str] = []


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None
    section: Section
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)


class FilterPosts(BaseModel):
    title: Union[str, None] = None
    tags: list[str] = []
    created_at_gt: Union[datetime, None] = None
    created_at_lt: Union[datetime, None] = None
    section_id: Union[int, None] = None

    @model_validator(mode="after")
    @classmethod
    def check_date_range(cls, values):
        created_at_gt, created_at_lt = values.created_at_gt, values.created_at_lt

        if created_at_gt and created_at_lt:
            if created_at_gt >= created_at_lt:
                raise ValueError("created_at_gt must be date before created_at_lt")

        return values

    model_config = ConfigDict(from_attributes=True)
