from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from pydantic import BaseModel
from models.products import Product, Productresponse
from db import SessionDep

router = APIRouter(
    prefix="/products",
    tags=["products"],
)



@router.get("/{id}")
async def get_products(id: int, session: SessionDep):
    product = session.get(Product, id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return Productresponse.model_validate(product)
 


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    return


@router.get("/search")
async def search_products(q: str = Query(None, min_length=3, max_length=50)):
    if q is None:
        raise HTTPException(status_code=400, detail="Parameter q is required")
    return
