from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from config import db_connection
from api_v1.exeptions import ValidationError


router = APIRouter(prefix='/users',
                   tags=['Users'],
                   )


@router.get(path='/get',
            description='Test end point',
            )
async def get_user(request: Request):
    return request.user
