from fastapi import APIRouter
from fastapishop.database import SessionDep
from fastapishop.models import UsersOrm
from fastapishop.security import get_current_user, password_hash, get_current_admin
from fastapishop.schemas import *
from fastapi import Depends
from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
async def get_me(current_user: UsersOrm = Depends(get_current_user)):
    user_data = UserResponse.model_validate(current_user)

    return user_data

@router.post("/")
async def users_create(user_data: UserCreate, sess: SessionDep):
    get_user_query = (
        select(UsersOrm)
        .where(UsersOrm.username == user_data.username)
    )
    result = await sess.execute(get_user_query)
    user = result.scalar_one_or_none()

    if user is not None:
        raise HTTPException(detail={"message":"error, user already exists"}, status_code=409)

    hashed_password = password_hash.hash(user_data.password)

    u_data = user_data.model_dump(exclude={"password"})
    u_data["hashed_password"] = hashed_password

    user = UsersOrm(**u_data)
    sess.add(user)

    await sess.commit()

    user_response = UserResponse.model_validate(user)

    return user_response

@router.patch("/password")
async def change_user_password(new_data: UserChangePass, sess: SessionDep, user: UsersOrm = Depends(get_current_user)):
    if new_data.new_password == new_data.old_password:
        raise HTTPException(detail="Same passwords got", status_code=400)

    hashed_pass = user.hashed_password

    if not password_hash.verify(new_data.old_password, hashed_pass):
        raise HTTPException(detail="Old password is incorrect", status_code=400)

    new_hashed_pass = password_hash.hash(new_data.new_password)

    user.hashed_password = new_hashed_pass
    await sess.commit()

    return "success"

@router.patch("/me")
async def edit_user_data(new_user_data: UserUpdate, sess: SessionDep, curr_user: UsersOrm = Depends(get_current_user)):
    new_u_data = new_user_data.model_dump(exclude_unset=True)

    if not new_u_data:
        return JSONResponse(content={"msg":"Error, fields empty"},status_code=400)


    for field, value in new_u_data.items():
        setattr(curr_user, field, value)

    await sess.commit()

    return {"msg":"Ok, user updated", "user": UserResponse.model_validate(curr_user)}

@router.get("/")
async def get_all_users(sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(UsersOrm)
    )

    result = await sess.execute(query)
    users_db = result.scalars().all()

    users_all = [
        UserResponse.model_validate(user) for user in users_db
    ]

    return users_all

@router.delete("/{user_id}")
async def users_delete(user_id: int, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(UsersOrm)
        .filter(UsersOrm.id == user_id)
    )

    result = await sess.execute(query)

    curr_user = result.scalar_one_or_none()

    if curr_user is not None:
        await sess.delete(curr_user)
        await sess.commit()
        return {"message" : f"User {user_id} deleted."}
    else:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, sess: SessionDep, admin: UsersOrm = Depends(get_current_admin)):
    query = (
        select(UsersOrm)
        .filter_by(id=user_id)
    )

    res = await sess.execute(query)
    found_user = res.scalar_one_or_none()

    if found_user is not None:
        current_user = UserResponse.model_validate(found_user)
        return current_user
    else:
        return JSONResponse(content={
            "error" : "User doesn't exist!"
        }, status_code=404)
