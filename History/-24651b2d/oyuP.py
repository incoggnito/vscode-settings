import logging

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserDelete, UserResponse

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    *,
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> User:
    """[summary]

    Args:
        user_in (UserCreate): [description]
        db (Session, optional): [description]. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        User: [description]
    """
    if group not in settings.ADMIN_GROUP:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")
    if crud.user.exists(db=db, obj_in=user_in):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail=f"User with UID {user_in.uid} or E-Mail {user_in.email} already exists!",
        )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def read_user(*, current_user=Depends(deps.get_current_user)) -> User:
    """[summary]

    Args:
        uid (int): [description]
        db (Session, optional): [description]. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: [description]

    Returns:
        User: [description]
    """
    # user = crud.user.get_by_uid(db=db, uid=uid)
    # if not user:
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND, detail=f"User with UID {uid} not found!"
    #     )
    return current_user  # user


@router.put("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
    *,
    user_in: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
) -> User:
    """_summary_

    Args:
        user_in (UserUpdate): _description_
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).
        current_user (_type_, optional): _description_. Defaults to Depends(deps.get_current_user).

    Returns:
        User: _description_
    """
    # if not db.query(db.query(User).filter(User.uid == uid).exists()).scalar():
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND, f"User with UID {uid} not found!"
    #     )
    user = crud.user.update(db=db, uid=current_user.uid, obj_in=user_in)
    return user


@router.get("/all/", status_code=status.HTTP_200_OK)
async def get_all_users(
    *,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> List[User]:
    if group not in settings.ADMIN_GROUP:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")

    users = crud.user.read_all(db=db)

    if not users:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"No users and contracts found!",
        )

    return users