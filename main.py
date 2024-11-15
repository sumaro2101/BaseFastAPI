from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import db_connection, BaseModel
from api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_connection.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        yield
    await db_connection.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
