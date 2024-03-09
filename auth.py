from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated

import uvicorn
import psycopg2 as pg
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

db = pg.connect(dbname="autolab", user="postgres", password="postgres", host="127.0.0.1")


class Status(Enum):
    STUDENT = 0
    TUTOR = 1
    ADMIN = 2
    MAIN_ADMIN = 3


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    role: int | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM auth WHERE username=\'{username}\'")
    print(cur.statusmessage)
    for row in cur:
        user_dict = {'id': row[0], 'username': row[1], 'hashed_password': row[2]}
        cur2 = db.cursor()
        cur2.execute(f"SELECT role_id FROM auth WHERE username=\'{username}\'")
        for row2 in cur2:
            user_dict["role"] = row2[0]
        cur2.execute(f"SELECT surname, first_name, patronymic FROM students WHERE user_id={user_dict['id']}")
        for row2 in cur2:
            user_dict["full_name"] = f"{row2[0]} {row2[1]} {row2[2]}"
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_auth_user(request: Request):
    session_id = request.cookies.get("Authorization")
    if not session_id:
        raise HTTPException(status_code=401)
    # return RedirectResponse("/login", status_code=302)
    if await get_current_user(session_id) is None:
        return False
    return True


@app.post("/auth")
async def login_for_access_token(login=Form(), password=Form()):
    user = authenticate_user(login, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # SESSION_DB[SESSION_ID] = login
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="Authorization", value=access_token)
    return response


@app.get("/users/me/", dependencies=[Depends(get_auth_user)], response_model=User)
async def read_users_me(request: Request):
    current_user = await get_current_user(request.cookies.get("Authorization"))
    return current_user
