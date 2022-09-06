import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.core.config import settings
from app.models.project_def import ProjectDef
from app.models.user import User
from app.models.project_user import ProjectUser
from app.schemas.project_def import *

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ProjectDefSimpleResponse],
)
async def read_all_projectdefs(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[ProjectDef]:
    projectdefs = crud.project_def.read_all(db)
    if not projectdefs:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No project definitions found in database!",
        )
    return projectdefs


@router.post("/", status_code=status.HTTP_200_OK, response_model=ProjectDefResponse)
async def create_project(
    project_def_in: ProjectDefCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    group: str = Depends(deps.get_user_group),
) -> ProjectDef:
    if group in settings.TL_GROUP:
        worker_ids = project_def_in.worker_ids
        del project_def_in.worker_ids
        user_list = db.query(User).filter(User.uid.in_(worker_ids)).all()
        query = db.query(ProjectDef).filter(
            ProjectDef.submitter_id == current_user.uid,
            ProjectDef.customer_id == project_def_in.customer_id,
            ProjectDef.project_id == project_def_in.project_id,
            ProjectDef.task_id == project_def_in.task_id,
        )
        if db.query(query.exists()).scalar():
            db_obj = query.first()
            project_def = crud.project_def.update(
                db=db, obj_in=project_def_in, db_obj=db_obj
            )
        else:
            project_def = crud.project_def.create(
                db=db, obj_in=project_def_in, uid=current_user.uid
            )
        for user in user_list:
            project_def.workers.append(user)
        db.add(project_def)
        db.commit()
        return project_def
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")


@router.post(
    "/{project_def_id}/workers",
    status_code=status.HTTP_200_OK,
    response_model=ProjectDefResponse,
)
async def create_project_user(
    workers: Workers,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> ProjectDef:
    if group in settings.TL_GROUP:
        db.query()