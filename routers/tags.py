from fastapi import APIRouter
from database import db
from crud import tags
from schemas.tags import TagWithPostsCount
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=List[TagWithPostsCount])
def get_tags(db: db):
    return tags.get_all_tags(db)
