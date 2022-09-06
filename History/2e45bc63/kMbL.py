import logging
from typing import Union, List

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.monthly import MonthCarry
from app.models.user import User
from app.schemas.monthly import *
from app.core.config import settings

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MonthlyResponse,
)
async def create_monthly(
    *,
    monthly_in: MonthlyCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Union[MonthCarry, List[MonthCarry]]:
    if not crud.monthly.exists(
        db, uid=current_user.uid, year=monthly_in.year, month=monthly_in.month
    ):
        return crud.monthly.create(db, monthly_in, uid=current_user.uid)
    else:
        monthly_old = crud.monthly.read(
            db=db,
            uid=current_user.uid,
            year=monthly_in.year,
            month=monthly_in.month,
        )
        dif_vac = monthly_in.vacation - monthly_old.vacation
        dif_flex = monthly_in.flextime - monthly_old.flextime
        if dif_vac != 0 or dif_flex != 0:
            futures = crud.monthly.get_futures(
                db, current_user.uid, monthly_in.year, monthly_in.month
            )
            if futures:
                return crud.monthly.update_futures(db, futures, dif_vac, dif_flex)


@router.get(
    "/{year}/{month}/",
    status_code=status.HTTP_200_OK,
    response_model=MonthlyResponse,
)
async def read_monthly(
    *,
    year: int,
    month: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> MonthCarry:
    monthly = crud.monthly.read(db, current_user.uid, year, month)
    if not monthly:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail=f"monthly carry from {year}-{month} for user {current_user.uid} not found!",
        # )
        monthly = crud.monthly.read_last(db=db, uid=current_user.uid)
    return monthly


@router.get(
    "/{year}/{month}/all/",
    status_code=status.HTTP_200_OK,
    response_model=List[MonthlyResponse],
)
async def read_all_monthly(
    *,
    year: int,
    month: int,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> List[MonthCarry]:
    monthly = crud.monthly.read_all(db, year=year, month=month)
    if group not in settings.ADMIN_GROUP:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")
    return monthly


@router.get(
    "/last/",
    status_code=status.HTTP_200_OK,
    response_model=MonthlyResponse,
)
async def read_last_monthly(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> MonthCarry:
    monthly = crud.monthly.read_last(db, current_user.uid)
    if not monthly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"last monthly carry for user {current_user.uid} not found!",
        )
    return monthly


@router.delete(
    "/{year}/{month}/{uid}",
    status_code=status.HTTP_200_OK,
)
async def delete_monthly(
    *,
    year: int,
    month: int,
    uid: int,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> None:

    if (group in ["HR"]) & (crud.monthly.exists(db, uid, year, month)):
        return crud.monthly.delete(db, uid, year, month)
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Monthly carry from {year}-{month} for user {uid} not found! Or not privileged!",
        )
