from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    expired: datetime


class Tokens(BaseModel):
    access: Token
    refresh: Token
