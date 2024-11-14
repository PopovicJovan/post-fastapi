from sqlalchemy import select, func

from models.tags import Tag as Tag_model
from exceptions import ModelNotFoundException
from models.tags import post_tags
from models.posts import Post
from schemas.tags import Tag, TagWithPostsCount
from sqlalchemy.orm import Session


def get_or_create_tags(db: Session, tag_names: list[str]) -> list[Tag_model]:
    unique_tag_names = list(set(tag_names))

    existing_tags_query = select(Tag_model).where(Tag_model.name.in_(unique_tag_names))
    existing_tags = db.scalars(existing_tags_query).all()

    existing_tag_names = {tag.name for tag in existing_tags}

    new_tag_names = set(unique_tag_names) - existing_tag_names
    new_tags = [Tag_model(name=name) for name in new_tag_names]

    db.add_all(new_tags)
    return existing_tags + new_tags


def get_all_tags(db: Session) -> list[TagWithPostsCount]:
    results = (
        db.query(Tag_model.id, Tag_model.name, func.count(post_tags.c.post_id).label("posts_count"))
        .outerjoin(post_tags, Tag_model.id == post_tags.c.tag_id)
        .group_by(Tag_model.id)
        .all()
    )

    return [
        TagWithPostsCount(
            id=tag.id,
            name=tag.name,
            posts_count=tag.posts_count
        ) for tag in results
    ]


def delete_tag(db: Session, tag_id: int) -> None:
    tag = db.query(Tag_model).get(tag_id)
    if not tag:
        raise ModelNotFoundException("Tag",tag_id)
    db.delete(tag)


def delete_unused_tags(db: Session) -> None:
    query = (
        db.query(Tag_model)
        .outerjoin(post_tags, Tag_model.id == post_tags.c.tag_id)
        .outerjoin(Post, post_tags.c.post_id == Post.id)
        .group_by(Tag_model.id)
        .having(func.count(Post.id) == 0)
    )
    unused_tags = db.scalars(query).all()
    for tag in unused_tags:
        delete_tag(db, tag.id)



