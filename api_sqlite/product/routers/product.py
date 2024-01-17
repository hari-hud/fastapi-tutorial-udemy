from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from api_sqlite.product.database import get_db
from api_sqlite.product import models
from api_sqlite.product import schema

router = APIRouter(tags=["Products"], prefix="/products")


@router.get()
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.get("/{id}", response_model=schema.DisplayProduct)
def get_one_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.delete("/{id}")
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete()
    db.commit()
    return {"Product deleted"}


@router.put("/{id}")
def update(id, request: schema.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        print("Product not found")
        pass
    product.update(request.dict())
    db.commit()
    return {"Product updated"}


@router.post(status_code=status.HTTP_201_CREATED, response_model=schema.DisplayProduct)
def add(reqeust: schema.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=reqeust.name, price=reqeust.price, desc=reqeust.desc, seller_id=1
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return reqeust
