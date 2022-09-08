from os import stat
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from internal.token import manager
from database import db_session
from database.models import User
from routers.helper import (
    check_if_user_exists, hash_pass
)


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

class UserPayload(BaseModel):
    email: str
    password: str


@router.get("/logged-user-details", status_code=status.HTTP_200_OK)
async def get_user_details(user=Depends(manager)):
    try:
        username = tuple(user)[0]
        db_obj = db_session.query(User).filter(User.email == username).first()
        if db_obj:
            response = {
                'username': db_obj.email,
                'is_active': db_obj.is_active
            }
            return response
        else:
            return "Username not found"
    except Exception:
        raise HTTPException(
                status_code=418, detail="Exception occurred while saving details"
            )

@router.post(
    "/add-user",
    tags=["User"],
    responses={417: {"description": "Exception Failed"}},
    status_code=status.HTTP_201_CREATED
)
async def add_user(data: UserPayload):
    user_exists = await check_if_user_exists(data.email)
    if(not user_exists):
        try:
            user_obj = User(
                email=data.email,
                hashed_password=await hash_pass(data.password)
            )
            db_session.add(user_obj)
            db_session.commit()
            return "User added successfully"
        except Exception:
            db_session.rollback()
            raise HTTPException(
                status_code=418, detail="Exception occurred while saving details"
            )
        
    else:
        raise HTTPException(
            status_code=409, detail="Username already taken"
        )
