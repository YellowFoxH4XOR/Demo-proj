from fastapi_login import LoginManager
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from database import db_session
from database.models import User
from conf import SECRET
from datetime import timedelta
from routers.helper import (
    decode_hash_pass
)


manager = LoginManager(SECRET, token_url='/token')


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    """This Function works as authenticator function

    Args:
        email (str): user email

    Returns:
        tuple/None: if true return tuple else return None
    """
    db_obj = db_session.query(User).filter(User.email == email).first()
    if(db_obj):
        return (db_obj.email, db_obj.hashed_password, db_obj.is_active, db_obj.id)
    return None


router = APIRouter(
    prefix="/token",
    tags=["Token"],
    responses={418: {"description": "I'm a teapot"}},
)

@router.post('/')
async def get_token(data: OAuth2PasswordRequestForm = Depends()):
    """Oauth implementation route

    Args:
        data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().

    Raises:
        InvalidCredentialsException: user no found
        InvalidCredentialsException: password is wrong
        InvalidCredentialsException: user is not active

    Returns:
        dict: access token
    """
    email = data.username
    password = data.password

    user_pass = load_user(email)
    if not user_pass:
        raise InvalidCredentialsException
    elif password != await decode_hash_pass(user_pass[1]):
        raise InvalidCredentialsException
    elif not user_pass[2]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email), expires=timedelta(minutes=30) # set to 30 mins but can be changed
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
