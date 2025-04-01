from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "question"

    # primary_key는 id를 기본 키(Primary Key)로 만든 다는 것
    # index=True는 해당 칼럼에 인덱스를 생성한다는 것
    # 데이터 타입이 Integer이고 기본키로 설정한 속성은 값이 자동으로 증가하므로, 데이터 저장할때 값을 세팅하지 않아도 된다.
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), nullable=False) # null 값을 허용하지 않으려면 nullable=False로 설정해야 한다
    content = Column(Text, nullable=False) # 글 내용처럼 글자 수를 제한할 수 없는 텍스트는 Text를 사용
    create_date = Column(DateTime, nullable=False)

    answers = relationship("Answer", back_populates="question") # Answer 모델의 question 속성을 참조한다.

# question_id
# - 해당 속성은 답변을 질문과 연결 하기 위해 추가한 속성
# - 질문의 id 속성이 내용상 필요 하다. 그리고, 모델을 서로 연결할 때 ForeignKey를 사용한다.
# question
# - 해당 속성은 답변 모델 에서 질문 모델을 참조 하기 위해 추가
# - answer.question.subject 처럼 질문의 제목을 참조할 수 있다.
# back_populates는 하나의 모델에서 변경된 것이 관계를 가지는 다른 쪽에서도 반영되도록 설정하는 것이다.
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

    # 답변을 질문과 연결하기 위한 추가 속성, 서로 연결할 때는 ForiegnKey를 사용한다.
    # Qustion 테이블의 id 칼럽과 연결이 된다.
    question_id = Column(Integer, ForeignKey("question.id"))
    #question = relationship("Question", back_ref="answers")
    # replationship()으로 question 속성을 생성하면, answer.question.subject 처럼 질문의 제목을 참조할 수 있다.
    # 연결과 참조는 다르다.
    question = relationship("Question", back_populates="answers") # Quesion 모델의 answers 속성을 참조한다.


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

'''
>>> a
<models.Answer object at 0x000001672C7CB860>
>>> a.question
<models.Question object at 0x000001672C642CC0>
>>> q
<models.Question object at 0x000001672C642CC0>
>>> q.answer
[<models.Answer object at 0x000001672C7CB860>] # InstrumentedList

>>> a.question.answer # Answer를 통해 Question을 갔다가, 다시 Answer로 돌아오는 건 가능
[<models.Answer object at 0x000001672C7CB860>]

>>> q.answer[0].question # Quesion에 연결된 Answer는 InstrumentedList 이다? 외래키 설정해서 그런가?
<models.Question object at 0x000001672C642CC0>

'''