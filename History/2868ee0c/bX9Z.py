from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

from .user import UserResponse
from .customer import CustomerResponse
from .project import ProjectResponse
from .task import TaskResponse
from .department import DepartmentResponse


class ProjectDefCreate(BaseModel):
    description: Optional[str]
    budget: Optional[float] = 0.0
    start: date
    end: date
    factor: float
    department_id: int
    customer_id: int
    project_id: int
    task_id: int
    worker_ids: List[int]


class Workers(BaseModel):
    pid: int
    uid: int


class ProjectDefExistsResponse(BaseModel):
    id: int


class ProjectDefRead(BaseModel):
    pass


class ProjectDefUpdate(BaseModel):
    pass


class ProjectDefDelete(BaseModel):
    pass


class ProjectDefResponse(BaseModel):
    id: int
    date_created: datetime
    description: Optional[str]
    budget: Optional[float] = 0.0
    start: datetime
    end: datetime
    factor: float
    department_id: int
    customer_id: int
    project_id: int
    task_id: int
    customer: CustomerResponse
    project: ProjectResponse
    task: TaskResponse

    class Config:
        orm_mode = True


class ProjectDefSimpleResponse(BaseModel):
    id: int
    customer: CustomerResponse
    project: ProjectResponse
    task: TaskResponse
    submitter_id: int
    budget: Optional[float]
    factor: Optional[float]
    start: Optional[datetime]
    end: Optional[datetime]
    department: Optional[DepartmentResponse]
    workers: Optional[List[UserResponse]]

    class Config:
        orm_mode = True


class Projecthours(BaseModel):
    id: int
    date_created: datetime
    description: Optional[str]
    duration: Optional[str]
    customer: CustomerResponse
    project: ProjectResponse
    task: TaskResponse

    class Config:
        orm_mode = True
