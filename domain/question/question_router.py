from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

#from database import SessionLocal

from models import Question
from database import get_db
from domain.question import question_schema

# router 객체를 생성하여 FastAPI 앱에 등록해야만 라우팅 기능이 동작한다.
router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def quesion_list(db: Session = Depends(get_db)):
    #db = SessionLocal()
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    #db.close() # 커넥션 풀을 종료, 세션 종료가 아니다.
    return _question_list
