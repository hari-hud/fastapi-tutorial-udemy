from fastapi import FastAPI
from . import schema
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post("/porduct")
def add(requst: schema.Product):
    return requst
