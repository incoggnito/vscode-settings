import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core.config import settings
from app.models.task import Task
from app.models.user import User
from app.schemas.task import *

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get("/task/", status_code=status.HTTP_200_OK, response_model=List[TaskResponse])
async def read_all_tasks(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Task]:
    tasks = crud.task.read_all(db)
    if not tasks:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No tasks found in database!",
        )
    return tasks


@router.post("/task/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(
    *,
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Task:
    if group in settings.TL_GROUP:
        if crud.task.exists(db, task_in):
            return crud.task.get_task_by_label(db, task_in.label)
        else:
            return crud.task.create(db, task_in)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied!"
        )
