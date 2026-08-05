
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import joinedload

from database import SessionDep
from models import CategoryOrm, UsersOrm, ProductOrm
from schemas import ProductCreate, ProductResponse, ProductUpdate
from sqlalchemy import select
from security import get_current_admin


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", status_code=201)
async def create_product(data: ProductCreate, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    cat_id = data.category_id

    query = (
        select(CategoryOrm)
        .where(CategoryOrm.id == cat_id)
    )

    res = await sess.execute(query)

    cat: CategoryOrm = res.scalar_one_or_none()

    if cat is None:
        raise HTTPException(status_code=404, detail={"message":"Category not found"})

    prod = ProductOrm(**data.model_dump())
    prod.category = cat

    sess.add(prod)

    await sess.commit()

    prod_response = ProductResponse.model_validate(prod)

    return prod_response

@router.get("/")
async def get_all_products(sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(ProductOrm)
        .options(joinedload(ProductOrm.category))
    )

    res = await sess.execute(query)

    products = res.scalars().all()

    products_resp = [ProductResponse.model_validate(prod) for prod in products]

    return products_resp

@router.patch("/{product_id}")
async def patch_product(product_id: int, data: ProductUpdate, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    prod_data = data.model_dump(exclude_unset=True)

    query = (
        select(ProductOrm)
        .where(ProductOrm.id == product_id)
        .options(joinedload(ProductOrm.category))
    )

    res = await sess.execute(query)

    current_product: ProductOrm = res.scalar_one_or_none()

    if current_product is None:
        raise HTTPException(status_code=404, detail={"message":"Product not found"})

    if "category_id" in prod_data:
        query_category = (
            select(CategoryOrm)
            .where(CategoryOrm.id == prod_data["category_id"])
        )

        res = await sess.execute(query_category)

        found_category = res.scalar_one_or_none()

        if found_category is None:
            raise  HTTPException(status_code=404, detail={"message":"Category not found"})

        current_product.category = found_category

    for attr, val in prod_data.items():
        if attr != "category_id":
            setattr(current_product, attr, val)

    await sess.commit()
    await sess.refresh(current_product)

    prod_response = ProductResponse.model_validate(current_product)
    return prod_response

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(ProductOrm)
        .where(ProductOrm.id == product_id)
    )

    res = await sess.execute(query)

    current_product = res.scalar_one_or_none()

    if current_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await sess.delete(current_product)
    await sess.commit()

    return {"message":"Product deleted"}