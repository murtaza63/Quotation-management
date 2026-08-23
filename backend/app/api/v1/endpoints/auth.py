from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService.register_user(db, user)


@router.post("/login", response_model=Token)
def login_user(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return UserService.login_user(
        db,
        from_data.username,
        from_data.password,
    )


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
