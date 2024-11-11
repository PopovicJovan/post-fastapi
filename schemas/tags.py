from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class TagBase(BaseModel):
    name: Annotated[str, Field(..., max_length=64, min_length=2)]


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    posts_count: Optional[int]

    model_config = ConfigDict(from_attributes=True)
