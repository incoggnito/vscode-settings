import logging

from typing import List

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, extract, aliased, func

from app import crud
from app.api import deps
from app.core.config import settings
from app.models.calendar import Calendar
from app.models.meta import Meta
from app.models.user import User
from app.models.department import Department
from app.schemas.project import *

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.get(
    "department/",
    status_code=status.HTTP_200_OK,
)
async def read_department_performance(
    *,
    db: Session = Depends(deps.get_db)
    # group: str = Depends(deps.get_user_group),
):
    # if group in settings.PRIVILEGED_GROUP:
    c = aliased(Calendar)
    subq = (
        select(
            extract(c.year, "year"),
            month,
            func.sum(c.duration).label("duration_sum"),
            c.submitter_id.label("uid"),

        )
        .group_by(Address.user_id)
        .subquery()
    )

    subq = (
    select(func.count(Address.id).label("count"), Address.user_id)
    .group_by(Address.user_id)
    .subquery()
)

stmt = (
    select(User.username, func.coalesce(subq.c.count, 0)).
    outerjoin(subq, User.id == subq.c.user_id)
)
    # TODO read all calendar
    stmt = select(
        extract(Calendar.startdate, "year"), extract(Calendar.startdate, "month")
    )
    # calendar = db.query(Calendar).filter(Department.id == 2).all()