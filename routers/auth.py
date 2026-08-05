from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends, APIRouter
from models import UsersOrm
from database import SessionDep
from schemas import TokenResponse
from security import password_hash, create_access_token
from sqlalchemy import select

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

@router.post("/login")
async def auth_login(
        sess: SessionDep,
        user_data: OAuth2PasswordRequestForm = Depends()
):
    query = (
        select(UsersOrm)
        .filter(UsersOrm.username == user_data.username)
    )

    result = await sess.execute(query)

    auth_user = result.scalar_one_or_none()

    if auth_user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not password_hash.verify(user_data.password, auth_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user_token = create_access_token(auth_user.id)

    return TokenResponse(
        access_token=user_token,
        token_type="bearer"
    )