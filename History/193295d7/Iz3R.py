import logging

from typing import List

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core.config import settings
from app.models.project import Project
from app.models.user import User
from app.schemas.project import *

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    "/project/",
    status_code=status.HTTP_200_OK,
    response_model=List[ProjectResponse],
)
async def read_all_projects(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Project]:
    project = crud.project.read_all(db)
    if not project:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No projects found in database!",
        )
    return project


@router.post(
    "/project/", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse
)
async def create_project(
    *,
    project_in: CreateProject,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Project:
    if group in settings.TL_GROUP:
        if crud.project.exists(db=db, obj_in=project_in):
            return crud.project.update(db=db, obj_in=project_in)
        else:
            return crud.project.create(db=db, obj_in=project_in)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied!"
        )