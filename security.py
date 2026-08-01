import os
from urllib.parse import uses_relative

import jwt
from dotenv import load_dotenv
from jwt import PyJWTError
from pwdlib import PasswordHash
from datetime import timezone, timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy import select

from fastapishop.database import SessionDep
from fastapishop.models import UsersOrm

from authx import AuthX, AuthXConfig

load_dotenv()

password_hash = PasswordHash.recommended()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(days=1)

    payload = {
        "sub" : str(user_id),
        "exp" : expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def get_current_user(sess: SessionDep, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Authorization failed")


    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Couldn't validate credentials")

    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Couldn't validate credentials")

    query = (
        select(UsersOrm)
        .filter(UsersOrm.id == user_id)
    )

    res = await sess.execute(query)
    user: UsersOrm = res.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Couldn't validate credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User not active")


    return user

async def get_current_admin(curr_admin: UsersOrm = Depends(get_current_user)):
    if not curr_admin.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    return curr_admin