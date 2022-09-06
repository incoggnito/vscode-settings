from pydantic import BaseModel
from app.models.u import User


class ProjectUserCreate(BaseModel):
    uid: int
    pid: int


class ProjectUserMultiple(BaseModel):
    pid: int
    uid: List[User]


class ProjectUserRead(BaseModel):
    pass


class ProjectUserUpdate(BaseModel):
    pass


class ProjectUserDelete(BaseModel):
    pass


class ProjectUserResponse(BaseModel):
    uid: int
    pid: int

    class Config:
        orm_mode = True
