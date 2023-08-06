from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True
        
class PostView(PostCreate):
    id: int
