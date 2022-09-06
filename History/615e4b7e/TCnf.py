from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .user import UserResponse
from .department import DepartmentResponse


#####################################################
#                     Base                          #
#####################################################


class MetaCreate(BaseModel):
    workhours: float
    workdays: int
    province: str
    vacation: float
    groups: str
    year: int
    month: int
    # submitter_id: int


class MetaCreateFull(BaseModel):
    workhours: float
    workdays: int
    province: str
    vacation: float
    groups: str
    year: int
    month: int
    submitter_id: int
    hourrate: float
    department_id: int


class MetaRead(BaseModel):
    pass


class MetaUpdate(BaseModel):
    workhours: Optional[float]
    workdays: Optional[int]
    province: Optional[str]
    vacation: Optional[float]
    groups: Optional[str]


class MetaDelete(BaseModel):
    pass


class MetaResponse(BaseModel):
    id: int
    date_created: datetime
    workhours: float
    workdays: int
    province: str
    vacation: float
    groups: str
    year: int
    month: int
    submitter_id: int
    hourrate: float
    department_id: int
    submitter: UserResponse
    department: DepartmentResponse

    class Config:
        orm_mode = True
