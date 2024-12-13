from fastapi import APIRouter


router = APIRouter(prefix='/auth',
                   tags=['Auth'],
                   )



@router.post(path='/login',
            )