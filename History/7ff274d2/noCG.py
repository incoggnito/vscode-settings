from pydantic import BaseModel
from datetime import datetime


class ProjectUserCreate(BaseModel):
    label: str


class ProjectUserRead(BaseModel):
    pass


class ProjectUserUpdate(BaseModel):
    pass


class ProjectUserDelete(BaseModel):
    pass


class ProjectUserResponse(BaseModel):
    id: int
    date_created: datetime
    label: str

    class Config:
        orm_mode = True
