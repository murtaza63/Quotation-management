from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session


from app.db.database import get_db

from app.repositories.user_repository import UserRepository

from app.schemas.user import UserCreate
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.schemas.user import UserLogin

router = APIRouter()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService.register_user(db, user)


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return UserService.login_user(db, user.email, user.password)


@router.get("/me")
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
