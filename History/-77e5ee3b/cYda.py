import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from typing import List, Dict

from app import crud
from app.api import deps
from app.core.config import settings
from app.schemas.tags import *

from app.models.tags import Hashtag
from app.models.user import User

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    "/tag-all/", status_code=status.HTTP_200_OK, response_model=List[TagsResponse]
)
async def get_all_tags(
    *,
    db: Session = Depends(deps.get_db),
) -> List[Hashtag]:
    tags = crud.tags.read_all(db)
    if not tags:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No hashtags found in database!",
        )
    return tags


@router.get(
    "/tag/",
    status_code=status.HTTP_200_OK,
    response_model=List[TagsResponse],
)
async def get_tags_for_uid(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Hashtag]:
    tags = crud.tags.get_tags_for_uid(current_user.uid, db)
    if not tags:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No hashtags found in database!",
        )
    return tags


@router.get(
    "/tag/{project_def_id}/projects/",
    status_code=status.HTTP_200_OK,
    response_model=List[TagsResponse],
)
async def get_tags_for_p_def_id(
    *,
    project_def_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Hashtag]:
    tags = crud.tags.get_tags_for_p_def_id(project_def_id, db)
    if not tags:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No hashtags found in database!",
        )
    return tags


@router.post(
    "/tag/synonyms/{project_def_id}/",
    status_code=status.HTTP_201_CREATED,
    # response_model=TagsResponse,
)
async def create_synonyms(
    *,
    synonyms_in: SynonymsCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Dict[str, int]:
    num_created, num_deleted = crud.tags.create_synonyms(
        db, synonyms_in, uid=current_user.uid
    )
    return {"num_created": num_created, "num_deleted": num_deleted}


@router.post("/tag/", status_code=status.HTTP_201_CREATED, response_model=TagsResponse)
async def create_tag(
    *,
    tags_in: TagsCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Hashtag:
    if group in settings.TL_GROUP:
        if not crud.tags.exists(db, tags_in):
            return crud.tags.create(db, tags_in)
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag {tags_in.label} already exists!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied!"
        )
