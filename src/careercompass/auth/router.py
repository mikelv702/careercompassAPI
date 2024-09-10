import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
import httpx
from sqlalchemy.orm import Session
from urllib.parse import urlencode

from ..settings import get_app_settings
from .schemas import AuthorizationResponse, GithubUser, Url
from ..user.crud import get_user_by_email
from ..dependency import get_db
from ..user.schemas import User
from ..schemas import Token as SendToken
from .helpers import create_access_token


logger = logging.getLogger(__name__)
settings = get_app_settings()


auth_router = APIRouter(tags=['Auth'])
github_client_id=settings.github_client_id
github_client_secret=settings.github_client_secret


@auth_router.get('/github-login', tags=['OAuth'])
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@auth_router.get('/github-code', tags=['OAuth'])
async def github_code(code: str):
    print(code)
    async with httpx.AsyncClient() as client:
        params = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code': code
        }
        headers = {'Accept':'application/json'}
        response = await client.post(url='https://github.com/login/oauth/access_token',
            params=params, headers=headers
        )
    response_json = response.json()
    logger.debug('Github Access Token request')
    logger.debug(response_json)
    access_token = response_json.get('access_token')
    async with httpx.AsyncClient() as client: 
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get('https://api.github.com/user', headers=headers)
    
    return response.json()

@auth_router.get('/login', tags=['OAuth'])
async def get_login_url() -> Url:
    github_login_url = "https://github.com/login/oauth/authorize"
    params = {
        'client_id': github_client_id,
        'redirect_uri': 'https://app.cc.cloud.engineerhub.xyz/github-auth'
    }
    return Url(url=f"{github_login_url}?{urlencode(params)}")


@auth_router.post('/github-auth', tags=['OAuth'])
async def github_authorize_user(body: AuthorizationResponse, db: Session = Depends(get_db) ):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': body.code,
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client: 
        response = await client.post(url="https://github.com/login/oauth/access_token", 
            params=params, headers=headers
        )
    response_json = response.json()
    access_token = response_json.get('access_token')
    async with httpx.AsyncClient() as client: 
        headers.update({'Authorization': f'Bearer {access_token}'})
        user_request = await client.get('https://api.github.com/user', headers=headers)
    print(user_request.json())
    github_user = GithubUser(**user_request.json())

    logging.info('Authorizing user through github')
    # Check if the user's email is in the DB
    db_user = get_user_by_email(db, github_user.email)
    if db_user is None: 
        logger.error(f"No user found with email {github_user.email}")
        # We can auto magically create the user and have them skip the signup. 
        raise HTTPException(status_code=501, detail="Creating user from oauth is not implemented")
    
    verified_user = User.from_orm(db_user)
    logging.info(f"User verified: {github_user.email}")
    logging.info(f"Creating access token for user: {verified_user.email}")
    access_token = create_access_token(
        data={"sub": verified_user.email}
    )

    return SendToken(access_token=access_token, token_type='bearer')
    