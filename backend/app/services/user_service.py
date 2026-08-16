from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.exceptions import EmailAlreadyExistsException
from app.core.hashing import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.exceptions import InvalidCredentialsException


class UserService:

    @staticmethod
    def register_user(db: Session, user: UserCreate):
        existing_user = UserRepository.get_by_email(db, user.email)

        if existing_user:
            raise EmailAlreadyExistsException(user.email)
        hashed_password = hash_password(user.password)

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            hashed_password=hashed_password,
        )
        return UserRepository.create(db, db_user)

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)

        if not user:
            raise InvalidCredentialsException()
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
        }
