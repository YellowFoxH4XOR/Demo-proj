from ast import Pass
import imp
from re import I
from conf import PASS_SALT
from database import db_session
from database.models import User

async def check_if_user_exists(username: str) -> bool:
    print(username)
    db_obj = db_session.query(User).filter(User.email == username).all()
    if(not db_obj):
        return False
    return True

async def hash_pass(password: str) -> str:
    return PASS_SALT + password

async def decode_hash_pass(password: str) -> str:
    return ''.join(password.split(sep='---')[1:])