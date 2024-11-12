from fastapi import FastAPI, Request
from database import Base, engine
from models import *
from routers import sections, posts, tags
import exceptions as e
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(sections.router)
app.include_router(posts.router)
app.include_router(tags.router)


@app.exception_handler(e.ModelNotFoundException)
async def validation_exception_handler(request: Request, exc: e.ModelNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "message": exc.message
        }),
    )

@app.exception_handler(e.ModelInUseError)
async def validation_exception_handler(request: Request, exc: e.ModelInUseError):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "message": exc.message
        }),
    )