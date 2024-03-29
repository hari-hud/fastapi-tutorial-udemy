from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List, Union
from uuid import UUID
from datetime import date, datetime, time, timedelta


app = FastAPI()


class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta


class Image(BaseModel):
    url: HttpUrl
    name: str


class Product(BaseModel):
    name: str = Field(example="phone")
    price: float = Field(
        title="Price of the item",
        description="This would be the price of  the item beiung added",
        gt=0,
    )
    discount: int
    discounted_price: float
    tags: Set[str]  # = Field(examples="[electronic, phones]")
    image: List[Image]

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "name": "phone",
    #             "price": 100,
    #             "discount": 10,
    #             "discounted_price": 0,
    #             "tags": ["electronics", "computers"],
    #             "image": [{"url": "http://image1", "name": "img1"}],
    #         }
    #     }


class Offer(BaseModel):
    name: str
    desc: str
    price: float
    products: List[Product]


class User(BaseModel):
    name: str
    email: str


@app.get(path="/")
def index():
    return "Hello, World!"


@app.get(path="/movies")
def movies():
    return {"Movies": ["movie1", "movie2"]}


# Path Parameter: parameters passed in path
@app.get(path="/profile/{user}")
def get_profile(user: str):
    return {f"This is a profile page for - {user}"}


# Query Parameter: When parameter is passed in func but not in path
# to make query params optional we can set their values to None.
# /products?id=1&price=100
@app.get("/products")
def products(id: int = 1, price: str = None):
    return {f"Product with an Id: {id} and price: {price}"}


# Query + Path parameter
# /profile/{id}/comments?commentid=123
@app.get("/profile/{id}/comments")
def comments(id: int, commentid: int):
    return {f"Profile page for user Id: {id} and comment: {commentid}"}


@app.post("/products/{id}")
def create_product(product: Product, id: str, category: str):
    product.discounted_price = product.price - (product.price * product.discount) / 100
    return {"id": id, "product": product, "category": category}


# passing two models to same request
@app.post("/purchase")
def create_product(product: Product, user: User):
    return {"product": product, "user": user}


@app.post("/addoffer")
def addoffer(offer: Offer):
    return offer


@app.post("/event")
def add_event(event: Event):
    return event


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
