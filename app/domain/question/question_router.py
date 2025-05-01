from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_
from starlette import status
from sqlalchemy.orm import Session

#from database import SessionLocal

from app.database import get_db
from app.domain.user.user_router import get_current_user
from app.models import Question, User, Answer
from app.domain.question import question_schema
from app.domain.question.question_schema import QuestionCreate, QuestionUpdate, QuestionDelete

# router 객체를 생성하여 FastAPI 앱에 등록해야만 라우팅 기능이 동작한다.
router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10,
                  keyword: str = ''):
    #db = SessionLocal()
    #_question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    total, _question_list = get_question_list(
        db, skip=page * size, limit=size, keyword=keyword
    )
    #db.close() # 커넥션 풀을 종료, 세션 종료가 아니다.
    return {
        'total': total,
        'question_list': _question_list
    }

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    _question = get_question(db, question_id)
    return _question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: QuestionCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    create_question(db=db, question_create=_question_create, user=current_user)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: QuestionUpdate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Question not found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not authorized to perform this action")
    update_question(db=db, db_question=db_question, question_update=_question_update)
    return None

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: QuestionDelete, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Question not found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not authorized to perform this action")
    delete_question(db=db, db_question=db_question)

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    vote_question(db, db_question=db_question, db_user=current_user)


# qustion_crud
# def get_question_list(db: Session, skip: int = 0, limit: int = 10):
#     _question_list = db.query(Question)\
#         .order_by(Question.create_date.desc())
#
#     total = _question_list.count()
#     _question_list = _question_list.offset(skip).limit(limit).all()
#     return total, _question_list # (전체 건수, 페이징 적용된 질문 목록)

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user) # pydantic 스키마로 부터 ORM을 만든다.
    db.add(db_question)
    db.commit()

def update_question(db: Session, db_question: Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_data = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()

def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()

# 검색 기능
def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |        # 질문제목
                    Question.content.ilike(search) |        # 질문내용
                    User.username.ilike(search) |           # 질문작성자
                    sub_query.c.content.ilike(search) |     # 답변내용
                    sub_query.c.username.ilike(search)      # 답변작성자
                    )
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)
'''
response_model=list[question_schema.Question] 의미는
quesion_list 함수의 리턴 값은 Question 스키마로 구성된 리스트 임을 의미
'''