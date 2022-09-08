from conf import PASS_SALT
from database import db_session
from database.models import User

async def check_if_user_exists(username: str) -> bool:
    """This function checks if a username is already taken or not

    Args:
        username (str): new username

    Returns:
        bool: true/false
    """
    db_obj = db_session.query(User).filter(User.email == username).all()
    if(not db_obj):
        return False
    return True

async def hash_pass(password: str) -> str:
    """This function is used to encode the user password
       Right now it just appends a salt as a prefix but this can
       be improved to using hashlib lib.

    Args:
        password (str): password supplied

    Returns:
        str: encoded password
    """
    return PASS_SALT + password

async def decode_hash_pass(password: str) -> str:
    """This Function decodes the hash password to real password to map it
       with user supplied values

    Args:
        password (str): hashed pass

    Returns:
        str: original pass
    """
    return ''.join(password.split(sep='---')[1:])
