from sqlalchemy import select
from models.tags import Tag
from schemas.tags import Tag as TagSchema
from sqlalchemy.orm import Session


def get_or_create_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    unique_tag_names = list(set(tag_names))

    existing_tags_query = select(Tag).where(Tag.name.in_(unique_tag_names))
    existing_tags = db.scalars(existing_tags_query).all()

    existing_tag_names = {tag.name for tag in existing_tags}

    new_tag_names = set(unique_tag_names) - existing_tag_names
    new_tags = [Tag(name=name) for name in new_tag_names]  # list comprehension

    db.add_all(new_tags)
    return existing_tags + new_tags


def get_all_tags(db: Session) -> list[TagSchema]:
    query = select(Tag)
    result = db.scalars(query).all()

    tags_with_post_count = [
        TagSchema(
            id=tag.id, name=tag.name,
            posts_count=len(tag.posts)
        ) for tag in result
    ]

    return tags_with_post_count
