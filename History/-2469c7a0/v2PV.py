import logging

from typing import List

from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import *
from app.core.config import settings

router = APIRouter()
LOGGER = logging.getLogger(__name__)


@router.post(
    "/customer/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse
)
async def create_customer(
    *,
    customer_in: CustomerCreate,
    db: Session = Depends(deps.get_db),
    group: str = Depends(deps.get_user_group),
) -> Customer:
    if group in settings.TL_GROUP:
        if crud.customer.exists(db=db, obj_in=customer_in):
            return crud.customer.update(db, obj_in=customer_in)
        else:
            return crud.customer.create(db=db, obj_in=customer_in)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Permission denied!")


@router.get(
    "/customer/{id}/", status_code=status.HTTP_200_OK, response_model=CustomerResponse
)
async def read_customer(
    *,
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Customer:
    customer = crud.customer.read(db=db, id=id)
    if not customer:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {id} not found!"
        )
    return customer


@router.get(
    "/customer/", status_code=status.HTTP_200_OK, response_model=List[CustomerResponse]
)
async def read_all_customers(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Customer]:
    customers = crud.customer.read_all(db)
    if not customers:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"No customers found in database!"
        )
    return customers
