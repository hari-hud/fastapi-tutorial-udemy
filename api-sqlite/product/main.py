from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import schema
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get("/products/{id}", response_model=schema.DisplayProduct)
def get_one_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@app.delete("/products/{id}")
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete()
    db.commit()
    return {"Product deleted"}


@app.put("/products/{id}")
def update(id, request: schema.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        print("Product not found")
        pass
    product.update(request.dict())
    db.commit()
    return {"Product updated"}


@app.post("/product", status_code=status.HTTP_201_CREATED)
def add(reqeust: schema.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=reqeust.name, price=reqeust.price, desc=reqeust.desc
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return reqeust
