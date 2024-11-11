from fastapi import FastAPI
from database import Base, engine
from models import *
from routers import sections, posts, tags


Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(sections.router)
app.include_router(posts.router)
app.include_router(tags.router)
