from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, hash_password
from app.repositories.user_repository import UserRepository
from app.models.user import User


class UserService:

    @staticmethod
    def login_user(db, email: str, password: str):

        user = UserRepository.get_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    def register_user(db: Session, user_data):
        existing_user = db.query(User).filter(User.email == user_data.email).first()

        if existing_user:
            raise ValueError("Email already registered")

        new_user = User(
            full_name=user_data.full_name,
            phone=user_data.phone,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            is_active=True,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
