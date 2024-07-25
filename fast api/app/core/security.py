# oauth2.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from ..utils.auth import token as token_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return token_utils.verify_token(token=token)
