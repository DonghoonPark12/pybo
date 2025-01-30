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
def question_list(db: Session = Depends(get_db)):
    #db = SessionLocal()
    #_question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    _question_list = get_question_list(db)
    #db.close() # 커넥션 풀을 종료, 세션 종료가 아니다.
    return _question_list

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    _question = get_question(db, question_id)
    return _question

def get_question_list(db: Session):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

'''
response_model=list[question_schema.Question] 의미는
quesion_list 함수의 리턴 값은 Question 스키마로 구성된 리스트 임을 의미
'''