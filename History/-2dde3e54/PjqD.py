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
    def create(
        self, db: Session, *, obj_in: ProjectUserCreate, uid: int
    ) -> ProjectUser:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = ProjectUser(submitter_id=uid, **obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read(self, db: Session, id: int) -> ProjectUser:
        return super().read(db, id)

    def read_all(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ProjectUser]:
        return super().read_all(db, skip=skip, limit=limit)

    def update(
        self,
        db: Session,
        *,
        db_obj: ProjectUser,
        obj_in: Union[ProjectUserUpdate, Dict[str, Any]],
    ) -> ProjectUser:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


project_def = CRUDProjectUser(ProjectUser)
