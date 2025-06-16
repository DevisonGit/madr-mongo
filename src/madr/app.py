from fastapi import FastAPI

from src.madr.auth.routes import router as auth_router
from src.madr.authors.routes import router as author_router
from src.madr.books.routes import router as book_router
from src.madr.database import get_motor_client
from src.madr.settings import settings
from src.madr.users.routes import router as users_router

app = FastAPI()


@app.on_event('startup')
async def startup_db_client():
    if not hasattr(app, 'mongodb'):
        db_name = settings.DATABASE_URL.split('/')[-1]
        app.mongodb_client = get_motor_client()
        app.mongodb = app.mongodb_client[db_name]


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(author_router)
app.include_router(book_router)


@app.get('/')
def read_root():
    return {'message': 'MADR'}
