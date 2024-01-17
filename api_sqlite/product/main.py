from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import schema
import models
from database import engine, get_db
from passlib.context import CryptContext
from routers import product


app = FastAPI(
    title="Products API",
    description="Get product details",
    terms_of_service="http://www.google.com",
    contact={
        "Developer": "Hari Hud",
        "Website": "http://www.google.com",
        "Email": "harihud@gmail.com",
    },
    license_info={"name": "XYZ", "url": "http://www.google.com"},
    docs_url="/api",  # change '/docs' to '/api'
    redoc_url=None,  # disable /redoc link
)

app.include_router(product.router)

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post(
    "/seller",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.DisplaySeller,
    tags=["Seller"],
)
def add(reqeust: schema.Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(reqeust.password)
    seller = models.Seller(name=reqeust.name, email=reqeust.email, password=hashed_pwd)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
