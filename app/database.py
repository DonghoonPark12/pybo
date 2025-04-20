from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

# sqlite3 데이터베이스의 파일을 의미하며 프로젝트 루트 디렉터리에 저장한다는 의미
SQLALCHEMY_DATABASE_URL = get_settings().database_url

# create_engine은 커넥션 풀을 생성
# 컨넥션 풀이란 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말한다.
# (컨넥션 풀은 데이터 베이스에 접속하는 세션수를 제어하고, 또 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용한다.)
engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    #connect_args={"check_same_thread": False}
)

# SessionLocal은 데이터베이스에 접속하기 위해 필요한 클래스
# create_ending, sessionmaker 등을 사용하는 것은 sqlalchemy 데이터베이스 사용하기 위한 규칙
# 주의)
# - autocommit=False인 경우에는 데이터를 잘못 저장했을 경우 rollback 사인으로 되돌리는 것이 가능하지만
# - autocommit=True인 경우에는 commit이 필요없는 것처럼 rollback도 동작하지 않는다는 점에 주의해야
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스는 데이터베이스 모델을 구성할 때 사용되는 클래스
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
