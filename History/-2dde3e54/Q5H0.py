from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_user import ProjectUser
from app.schemas.project_user import *

from fastapi.encoders import jsonable_encoder


class CRUDProjectUser(
    CRUDBase[
        ProjectUser,
        ProjectUserCreate,
        ProjectUserRead,
        ProjectUserUpdate,
        ProjectUserResponse,
    ]
):
    def create(self, db: Session, *, obj_in: ProjectUserCreate) -> ProjectUser:
        return super().create(db, obj_in=obj_in)
        db.query(User).filter(User.uid == uid)


projectuser = CRUDProjectUser(ProjectUser)
