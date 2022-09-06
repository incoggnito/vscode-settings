import logging

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api import deps
from app.core.config import settings
from app.schemas.meta import MetaCreate, MetaUpdate, MetaDelete, MetaResponse
from app.models.meta import Meta
from app.models.user import User


router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MetaResponse)
async def create_meta(
    meta_in: MetaCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Meta:
    """_summary_

    Args:
        meta_in (MetaCreate): _description_
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        group (str, optional): _description_. Defaults to Depends(deps.get_user_group).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        Meta: _description_
    """
    if group in settings.PRIVILEGED_GROUP:
        meta = crud.meta.create(db=db, obj_in=meta_in)
        if not meta:
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail=f"Meta could not be created!"
            )
        else:
            return meta
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"Permission denied!")


@router.post("/{uid}", status_code=status.HTTP_201_CREATED, response_model=MetaResponse)
async def create_meta_by_uid(
    meta_in: MetaCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Meta:
    if group in settings.PRIVILEGED_GROUP:
        meta = crud.meta.create(db=db, obj_in=meta_in)
        if not meta:
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail=f"Meta could not be created!"
            )
        else:
            return meta
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"Permission denied!")


@router.get(
    "/{year}/{month}/",
    status_code=status.HTTP_200_OK,
    response_model=MetaResponse,
)
async def read_meta(
    year: int,
    month: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Meta:
    """_summary_

    Args:
        year (int): _description_
        month (int): _description_
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        current_user (User, optional): _description_. Defaults to Depends(deps.get_current_user).

    Raises:
        HTTPException: _description_

    Returns:
        Meta: _description_
    """
    meta = crud.meta.read(db=db, uid=current_user.uid, year=year, month=month)
    if not meta:
        """raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Meta information from {year}-{month} for User with UID {current_user.uid} not found!",
        )"""
        meta = crud.meta.get_latest_by_uid(db=db, uid=current_user.uid)
    return meta


@router.put(
    "/{year}/{month}/",
    status_code=status.HTTP_200_OK,
    response_model=MetaResponse,
)
async def update_meta(
    year: int,
    month: int,
    meta_in: MetaUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Meta:
    """_summary_

    Args:
        year (int): _description_
        month (int): _description_
        meta_in (MetaUpdate): _description_
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        current_user (User, optional): _description_. Defaults to Depends(deps.get_current_user).

    Raises:
        HTTPException: _description_

    Returns:
        Meta: _description_
    """
    if not crud.meta.exists(db=db, uid=current_user.uid, year=year, month=month):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Meta information with ID {meta_in.id} for user with UID {current_user.uid} not found!",
        )
    return crud.meta.update(
        db=db, uid=current_user.uid, year=year, month=month, obj_in=meta_in
    )


@router.put(
    "/{year}/{month}/{uid}",
    status_code=status.HTTP_200_OK,
    response_model=MetaResponse,
)
async def update_meta_by_uid(
    year: int,
    month: int,
    uid: int,
    meta_in: MetaUpdate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Meta:
    if group not in settings.PRIVILEGED_GROUP:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")
    if not crud.meta.exists(db=db, uid=uid, year=year, month=month):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Meta information with ID {meta_in.id} for user with UID {uid} not found!",
        )
    return crud.meta.update(db=db, uid=uid, year=year, month=month, obj_in=meta_in)


@router.get("/all/", status_code=status.HTTP_200_OK, response_model=List[MetaResponse])
async def get_all_meta(
    *,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> List[Meta]:
    if group not in settings.PRIVILEGED_GROUP:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")

    meta_data = crud.meta.read_all(db=db)

    if not meta_data:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No users and contracts found!",
        )

    return meta_data
