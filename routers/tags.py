from fastapi import APIRouter

from crud.tags import delete_unused_tags
from database import db
from crud import tags
from schemas.tags import TagWithPostsCount
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=List[TagWithPostsCount])
def get_tags(db: db):
    delete_unused_tags(db)
    db.commit()
    return tags.get_all_tags(db)
