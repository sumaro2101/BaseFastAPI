from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from config import db_connection
from api_v1.exeptions import ValidationError


router = APIRouter(prefix='/users',
                   tags=['Users'],
                   )


@router.get(path='/get',
            description='Test end point',
            )
async def get_user(
    session: AsyncSession = Depends(db_connection.session_geter),
):
    session = session
    raise ValidationError(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=dict(some='Some is wrong'))
