from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserRegister
from app.services.auth_service import register


router = APIRouter()


@router.post(
    "/register"
)
def register_route(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return register(user, db)