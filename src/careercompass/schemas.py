from pydantic import BaseModel


# Authentication and Tokens
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class ErrorResponse(BaseModel):
    detail: str
