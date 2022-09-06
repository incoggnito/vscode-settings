from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_user import ProjectUser
from app.models.user import User
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
        obj_in_data = jsonable_encoder(obj_in)
        uid = db.query(User).filter(User.uid == obj_in_data["uid"]).first().uid
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


projectuser = CRUDProjectUser(ProjectUser)
