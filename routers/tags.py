from fastapi import APIRouter
from sqlalchemy.testing.plugin.plugin_base import logging

from database import db
from crud import tags
from schemas import tags as tag_schema
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("")
def get_tags(db: db):
    return tags.get_all_tags(db)
