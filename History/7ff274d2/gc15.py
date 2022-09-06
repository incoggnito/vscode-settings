from pydantic import BaseModel
from datetime import datetime


class ProjectUserCreate(BaseModel):
    uid: int
    pid: int


class ProjectUserMultiple(BaseModel):
    uid: int
    pid: List[User]


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
