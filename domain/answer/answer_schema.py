import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: Optional[User]
    question_id: int
    modify_date: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int

'''
Q. 입력 항목을 처리하는 스키마는 왜 필요할까?
- 답변 등록 API는 post 방식이고, content라는 입력 항목이 있다.
- 답변 등록 라우터에서 content 값을 읽기 위해서는 반드시 content 항목을 포함하는 Pydantic 스키마를 통해 읽어야 한다.
- 스키마를 사용하지 않고, 라우터 함수의 매개변수에 content: str을 추가하여 값을 읽을 수 없다.
- 왜냐하면 get 방식이 아닌, post, put, delete 방식은 (body에 데이터를 담아 보내며) Pydantic 스키마를 통해 읽어야 하기 때문이다.
- 반대로 get 방식은 query parameter로 데이터를 전달하기 때문에 Pydantic 스키마를 사용하지 않아도 된다. 
  Pydanctic 스키마로 읽을 수 없고, 각각의 입력 항목을 라우터 함수의 매개변수로 읽어야 한다.
'''