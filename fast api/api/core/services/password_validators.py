import re
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator


def check_min_length(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return v


def check_uppercase(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    return v


def check_lowercase(v: str) -> str:
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    return v


def check_digit(v: str) -> str:
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one digit")
    return v


def check_special_char(v: str) -> str:
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("Password must contain at least one special character")
    return v


ValidatedPassword = Annotated[
    str,
    AfterValidator(check_min_length),
    AfterValidator(check_uppercase),
    AfterValidator(check_lowercase),
    AfterValidator(check_digit),
    AfterValidator(check_special_char),
]
