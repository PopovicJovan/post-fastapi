from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Query, UploadFile
import crud.posts as posts
from exceptions import ModelNotFoundException
from schemas.posts import FilterPosts, Post, PostCreate, PostPut, PostPatch
from database import db
from typing import List
from fastapi import File
router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=List[Post])
def list_posts(db: db, filters: Annotated[FilterPosts, Query()]):
    try: return posts.list_posts(db, filters)
    except ModelNotFoundException as e: raise e


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: db):
    try: return posts.get_post(db, post_id)
    except ModelNotFoundException as e: raise e


@router.post("", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: db):
    try:
        post = posts.create_post(db=db, post_data=post)
        db.commit()
        db.refresh(post)
        return post
    except ModelNotFoundException as e: raise e


@router.patch("/{post_id}/image-upload", response_model=None, status_code=201)
def upload_image(db: db, post_id: int, image: UploadFile = File(...)):
    try:
        posts.upload_image(db=db, image=image, post_id=post_id)
        db.commit()
    except ModelNotFoundException as e: raise e

@router.put("/{post_id}", response_model=Post)
def update_put_post(post_id: int, post: PostPut, db: db):
    try:
        post = posts.update_post(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except ModelNotFoundException as e: raise e


@router.patch("/{post_id}", response_model=Post)
def update_patch_post(post_id: int, post: PostPatch, db: db):
    try:
        post = posts.update_post(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except ModelNotFoundException as e: raise e

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: db):
    try:
        posts.delete_post(db, post_id)
        db.commit()
    except ModelNotFoundException as e: raise e

