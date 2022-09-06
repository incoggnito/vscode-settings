from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from .user import UserResponse


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
    submitter: UserResponse

    class Config:
        orm_mode = True
