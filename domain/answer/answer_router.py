from datetime import datetime
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models import Question, Answer
from domain.answer.answer_schema import AnswerCreate
from domain.question.question_router import get_question

router = APIRouter(
    prefix="/api/answer",
)

@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, _answer_create: AnswerCreate, db: Session = Depends(get_db)):
    '''
    - 프론트엔드에서 API 호출시 파라미터로 전달한 content가 AnswerCreate 스키마에 자동으로 매핑된다.
    - 출력은 response_model을 사용하는 대신 status_code=status.HTTP_204_NO_CONTENT 를 사용했다.
    - 이렇게 리턴할 응답이 없을 경우에는 응답코드 204를 리턴하여 "응답 없음"을 나타낼 수 있다.
    '''
    # Create answer
    question = get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    create_answer(db, question=question, answer_create=_answer_create)


def create_answer(db: Session, question: Question, answer_create: AnswerCreate):
    db_answer = Answer(question=question, content=answer_create.content, create_date=datetime.now())
    db.add(db_answer)
    db.commit()
