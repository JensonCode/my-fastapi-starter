from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..config import jwt_config
from ..database.database import session
from ..models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=jwt_config["access_token_expire_minutes"]
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_config["secret_key"], algorithm=jwt_config["algorithm"]
    )
    return encoded_jwt


def verify_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token, jwt_config["secret_key"], algorithms=[jwt_config["algorithm"]]
        )
        return payload.get("sub")
    except JWTError:
        return None


async def auth(
    token: str = Depends(oauth2_scheme), db: Session = Depends(session)
) -> User:
    not_authenticated_exception = HTTPException(
        status_code=401, detail="Not authenticated"
    )

    sub = verify_access_token(token)
    if not sub:
        raise not_authenticated_exception

    user = db.query(User).filter(User.username == sub).first()
    if not user:
        raise not_authenticated_exception

    return user
