from pydantic import BaseModel
from datetime import datetime


class ProjectUserCreate(BaseModel):
    label: str


class DepartmentRead(BaseModel):
    pass


class DepartmentUpdate(BaseModel):
    pass


class DepartmentDelete(BaseModel):
    pass


class DepartmentResponse(BaseModel):
    id: int
    date_created: datetime
    label: str

    class Config:
        orm_mode = True
