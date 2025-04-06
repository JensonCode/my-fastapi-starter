from fastapi import Depends
from sqlalchemy.orm import Session
from ..database.database import session
from ..deps.bcrypt import Bcrypt
from ..models.user import User
from ..schemas.user import RegisterFormData


class UserService:
    def __init__(self, db: Session = Depends(session)):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_password_hash(self, password: str) -> str:
        return Bcrypt.hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return Bcrypt.verify_password(plain_password, hashed_password)

    def create_user(self, register: RegisterFormData = Depends()) -> User:
        hashed_password = self.get_password_hash(register.password)
        new_user = User(username=register.username, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
