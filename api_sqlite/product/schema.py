from pydantic import BaseModel


class Seller(BaseModel):
    name: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    name: str
    desc: str
    price: int


class DisplayProduct(BaseModel):
    name: str
    desc: str
    seller: DisplaySeller

    class Config:
        orm_mode = True
