from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    name: Annotated[str, Field(..., max_length=64, min_length=2)]


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)