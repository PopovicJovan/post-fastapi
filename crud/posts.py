from typing import Optional, Union
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from crud.sections import get_section
from crud.tags import get_or_create_tags
from exceptions import ModelNotFoundException
from models.posts import Post
from models.tags import Tag
from schemas.posts import FilterPosts, PostCreate, PostPut, PostPatch
from uuid import uuid4

IMAGE_DIR = "public/images/posts/"

def get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise ModelNotFoundException("Post", post_id)
    return post


def list_posts(db: Session, filters: Optional[FilterPosts] = None) -> list[Post]:
    query = select(Post)

    if filters:
        if filters.title:
            query = query.where(Post.title.ilike(f"%{filters.title}%"))
        if filters.created_at_gt:
            query = query.where(Post.created_at >= filters.created_at_gt)
        if filters.created_at_lt:
            query = query.where(Post.created_at <= filters.created_at_lt)
        if filters.tags:
            query = query.where(Post.tags.any(or_(*[Tag.name == tag for tag in filters.tags])))
        if filters.section_id is not None:
            try: section = get_section(db, filters.section_id)
            except ModelNotFoundException:
                raise ModelNotFoundException("Section", filters.section_id)
            query = query.where(Post.section_id == section.id)
    return list(db.scalars(query).all())


def create_post(db: Session, post_data: PostCreate) -> Post:
    section = get_section(db, post_data.section_id)

    new_post = Post(**post_data.model_dump(exclude={"tags"}))
    new_post.section = section

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        new_post.tags = tags

    db.add(new_post)
    return new_post


def upload_image(db: Session, image: UploadFile, post_id: int) -> None:
    post = get_post(db, post_id)
    image.filename = str(uuid4())
    post.image = image.filename
    contents = image.file.read()
    with open(f"{IMAGE_DIR}{post.image}.jpg", "wb") as f:
        f.write(contents)
        f.flush()
        f.close()

def update_post(db: Session, post_id: int, post_data: Union[PostPut, PostPatch]) -> Union[Post, dict]:
    post_being_updated = get_post(db, post_id)

    if post_data.section_id is not None:
        section = get_section(db, post_data.section_id)

    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})

    for key, value in update_data.items():
        setattr(post_being_updated, key, value)

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        post_being_updated.tags = tags

    return post_being_updated


def delete_post(db: Session, post_id: int) -> None:
    post = get_post(db, post_id)
    db.delete(post)