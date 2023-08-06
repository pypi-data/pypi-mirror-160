from fastapi import FastAPI
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from database import engine,Base,SessionLocal
from models import Post
from schemas import PostView,PostCreate


app = FastAPI()

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
        
Base.metadata.create_all(bind=engine)

router = SQLAlchemyCRUDRouter(
    schema=PostView,
    create_schema=PostCreate,
    db_model=Post,
    db=get_db,
    prefix='posts',
    delete_all_route = False,
    delete_one_route = False,
    create_route = False,
    update_route = False
)
app.include_router(router)
