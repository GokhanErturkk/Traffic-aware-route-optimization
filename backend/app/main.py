from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import path
from .config import settings
from .customErrors import CustomError
from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(CustomError)
async def custom_error_handler(request, exc):
    return JSONResponse(content={"msg": exc.detail}, status_code=exc.status_code)


app.include_router(path.router)

@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
