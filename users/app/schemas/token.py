from typing import Literal, Optional

from pydantic import BaseModel
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class TokenPayload(BaseModel):
    user_id: Optional[UUID]
