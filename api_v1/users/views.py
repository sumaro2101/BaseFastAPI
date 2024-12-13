from fastapi import APIRouter, Request


router = APIRouter(prefix='/users',
                   tags=['Users'],
                   )


@router.get(path='/get',
            description='Test end point',
            )
async def get_user(request: Request):
    return request.user
