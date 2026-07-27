from fastapi.exceptions import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette.responses import JSONResponse

from fastapishop.schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from fastapishop.database import SessionDep
from fastapishop.models import CategoryOrm, UsersOrm
from fastapishop.security import get_current_admin

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/")
async def get_all_categories(sess: SessionDep):
    query = (
        select(CategoryOrm)
    )

    res = await sess.execute(query)

    cats = res.scalars().all()

    cats_response = [CategoryResponse.model_validate(cat) for cat in cats]

    return cats_response

@router.post("/")
async def create_category(category_data: CategoryCreate, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    data = category_data.model_dump()

    new_category = CategoryOrm(**data)

    sess.add(new_category)

    await sess.commit()

    return JSONResponse(status_code=201,content={"message":"Category created"})

@router.patch("/{cat_id}")
async def edit_category(cat_id: int, category_data: CategoryUpdate, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(CategoryOrm)
        .where(CategoryOrm.id == cat_id)
    )
    res = await sess.execute(query)

    curr_category: CategoryOrm = res.scalar_one_or_none()

    if curr_category is None:
        raise HTTPException(status_code=404, detail={"message":"Category not found"})

    if curr_category.name == category_data.name:
        raise HTTPException(status_code=400, detail={"message":"Category name is already the same"})

    curr_category.name = category_data.name

    await sess.commit()

    resp = CategoryResponse.model_validate(curr_category)

    return resp

@router.delete("/{cat_id}")
async def delete_category(cat_id: int, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(CategoryOrm)
        .where(CategoryOrm.id == cat_id)
        .options(selectinload(CategoryOrm.products))
    )

    res = await sess.execute(query)

    category: CategoryOrm = res.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail={"message":"Category not found"})

    if category.products:
        raise HTTPException(status_code=409, detail={"message":"Products in this category"})

    await sess.delete(category)
    await sess.commit()
    return {"message":f"Category {cat_id} deleted"}
