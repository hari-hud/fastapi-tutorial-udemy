from pydantic import BaseModel


class Product(BaseModel):
    name: str
    desc: str
    price: int


class DisplayProduct(BaseModel):
    name: str
    desc: str

    class Config:
        orm_mode = True
