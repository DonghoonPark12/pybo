from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True) # primary_key는 id를 기본 키(Primary Key)로 만든 다는 것
    subject = Column(String(100), nullable=False) # null 값을 허용하지 않으려면 nullable=False로 설정해야 한다
    content = Column(Text, nullable=False) # 글 내용처럼 글자 수를 제한할 수 없는 텍스트는 Text를 사용
    create_date = Column(DateTime, nullable=False)

    answer = relationship("Answer", back_populates="question")

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
    create_data = Column(DateTime, nullable=False)

    question_id = Column(Integer, ForeignKey("questions.id"))
    #question = relationship("Question", back_ref="answers")
    question = relationship("Question", back_populates="answer")