from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from ..services import Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    return Token.verify_token(token=token)
