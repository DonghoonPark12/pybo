from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from database import get_db
from domain.answer import answer_schema
from domain.user.user_router import get_current_user
from models import Question, Answer, User
from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from domain.question.question_router import get_question

router = APIRouter(
    prefix="/api/answer",
)

@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(question_id: int, _answer_create: AnswerCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    '''
    Description
        - 프론트엔드에서 API 호출시 파라미터로 전달한 content가 AnswerCreate 스키마에 자동으로 매핑된다.
        - 출력은 response_model을 사용하는 대신 status_code=status.HTTP_204_NO_CONTENT 를 사용했다.
        - 이렇게 리턴할 응답이 없을 경우에는 응답코드 204를 리턴하여 "응답 없음"을 나타낼 수 있다.
    '''
    # Create answer
    question = get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    create_answer(db, question=question, answer_create=_answer_create, user=current_user)

@router.post("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = get_answer(db, answer_id=answer_id)
    return answer

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(_answer_update: answer_schema.AnswerUpdate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    update_answer(db=db, db_answer=db_answer, answer_update=_answer_update)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(_answer_delete: answer_schema.AnswerDelete,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_answer = get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_answer.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    delete_answer(db=db, db_answer=db_answer)

# answer_crud
def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question, content=answer_create.content, create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
    db.commit()

def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)

def update_answer(db: Session, db_answer: Answer,
                  answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_data = datetime.now()
    db.add(db_answer)
    db.commit()

def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()

