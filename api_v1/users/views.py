from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from config import db_connection


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
    return {'user': 'is_work'}
