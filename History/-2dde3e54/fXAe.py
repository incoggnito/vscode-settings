from typing import List, Union, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_def import ProjectDef
from app.schemas.project_def import *

from fastapi.encoders import jsonable_encoder


class CRUDProjectUser(
    CRUDBase[
        ProjectDef,
        ProjectDefCreate,
        ProjectDefRead,
        ProjectDefUpdate,
        ProjectDefResponse,
    ]
):
    def create(self, db: Session, *, obj_in: ProjectDefCreate, uid: int) -> ProjectDef:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = ProjectDef(submitter_id=uid, **obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read(self, db: Session, id: int) -> ProjectDef:
        return super().read(db, id)

    def read_all(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ProjectDef]:
        return super().read_all(db, skip=skip, limit=limit)

    def update(
        self,
        db: Session,
        *,
        db_obj: ProjectDef,
        obj_in: Union[ProjectDefUpdate, Dict[str, Any]],
    ) -> ProjectDef:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)


project_def = CRUDProjectDef(ProjectDef)
