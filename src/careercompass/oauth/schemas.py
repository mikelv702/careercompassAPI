from pydantic import BaseModel

class Url(BaseModel):
    url: str

class AuthorizationResponse(BaseModel):
    code: str

class GithubUser(BaseModel):
    login: str
    name: str
    company: str
    location: str
    email: str
    avatar_url: str