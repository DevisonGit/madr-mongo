from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.auth.schemas import Token
from src.madr.auth.service import create_token_service, refresh_token_service
from src.madr.database import get_session
from src.madr.security import get_current_user
from src.madr.users.models import User

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2, session: Session):
    return await create_token_service(form_data, session)


@router.post('/refresh-token', response_model=Token)
def refresh_access_token(current_user: CurrentUser):
    return refresh_token_service(current_user)
