from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.domain.user.user_schema import UserCreate
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    #db_user = User(**user_create.dict()) # 이렇게 하기 위해서는 ORM과 Pydantic 인자가 모두 동일해야 한다.
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()