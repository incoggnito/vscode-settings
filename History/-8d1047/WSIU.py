import logging

from typing import List

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

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
    stmt = text(
        """ SELECT v.year,
    v.month,
    v.duration_sum,
    v.uid,
    v.pid,
    m.hourrate,
    p.factor,
    p.budget,
    p.start,
    p."end",
    id_c.label AS costumer,
    id_p.label AS projekt,
    id_t.label AS task
   FROM ( SELECT date_part('year'::text, tbl_calendar.startdate) AS year,
            date_part('month'::text, tbl_calendar.startdate) AS month,
            sum(tbl_calendar.duration) AS duration_sum,
            tbl_calendar.submitter_id AS uid,
            tbl_calendar.project_def_id AS pid
           FROM tbl_calendar
          GROUP BY tbl_calendar.submitter_id, (date_part('year'::text, tbl_calendar.startdate)), (date_part('month'::text, tbl_calendar.startdate)), tbl_calendar.project_def_id
          ORDER BY tbl_calendar.submitter_id, (date_part('year'::text, tbl_calendar.startdate)), (date_part('month'::text, tbl_calendar.startdate))) v
     LEFT JOIN tbl_meta m ON v.uid = m.submitter_id AND v.year = m.year::double precision AND v.month = m.month::double precision
     LEFT JOIN tbl_projectdef p ON v.pid = p.id
     LEFT JOIN tbl_customer id_c ON p.customer_id = id_c.id
     LEFT JOIN tbl_project id_p ON p.project_id = id_p.id
     LEFT JOIN tbl_task id_t ON p.task_id = id_t.id;"""
    )

    r = db.execute(stmt)
    # calendar = db.query(Calendar).filter(Department.id == 2).all()