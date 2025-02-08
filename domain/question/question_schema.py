import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []

    class Config:
        from_attributes = True # orm 모드를 활성화 하면, 모델의 항목이 자동으로 스키마로 매핑된다.

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

'''
models.py 파일에 정의한 Question 클래스는 Question 모델이라 하겠다.
pydantic의 BaseModel을 상속한 Question 클래스를 앞으로 Question 스키마라 하겠다.

(Pydantic을 이용한) Schema를 사용하는 것은
입출력 값이 정확한지 검증하는 것 외에, DB에 저장하는 것과 실제 고객에 응답으로 전달하는 것을 다르게 하는 의미도 있다.

e.g.
Quesion 스키마에서 content를 삭제할 수도 있다. 
다만, orm에서는 내부 구현용으로 남겨 놓을 수 있다.
'''