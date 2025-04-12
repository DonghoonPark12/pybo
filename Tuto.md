## ORM(object relational mapping)
- 데이터 베이스를 다루려면 쿼리문을 작성하고 실행하는 등의 방법이 필요하다.
- ORM을 이용하면 파이썬 문법만으로도 데이터베이스를 다룰 수 있다
- ORM은 데이터베이스의 테이블을 파이썬 클래스로 매핑해주는 것이다.
- 데이터를 관리하는 데 사용하는 ORM 클래스를 모델이라고 한다

## 예시1
```
id	subject	content
1	안녕하세요	가입 인사드립니다 ^^
2	질문 있습니다	ORM이 궁금합니다
...	...	...
```
```
insert into question(subject, content) values('안녕하세요', '가입 인사드립니다 ^^');
insert into question(subject, content) values('질문 있습니다', 'ORM이 궁금합니다');
```
```
question1 = Question(subject='안녕하세요', content='가입 인사드립니다 ^^')
question2 = Question(subject='질문 있습니다', content='ORM이 궁금합니다')
```

---
### (1) back_pupulate vs backref
- backref는 한쪽만 설정해주면 되고, back_populate는 양쪽 모두 설정해주어야 한다.
- 세밀한 제어가 필요할 때 back_populate를 사용한다.
```
children = relationship("Child", back_populates="parent")  # on the parent class
and
parent = relationship("Parent", back_populates="children")  # on the child class


children = relationship("Child", backref="parent")  # only on the parent class
or
parent = relationship("Parent", backref="children")  # only on the child class
```
- 아래에 따르면 .back_populates가 선호 된다고 나와 있다.
- 참조: https://stackoverflow.com/questions/51335298/concepts-of-backref-and-back-populate-in-sqlalchemy
- 참조: https://docs.sqlalchemy.org/en/14/orm/backref.html

---
### (2) alembic
- alembic은 SQLAlchemy로 작성한 모델을 기반으로 데이터베이스를 쉽게 관리할 수 있게 도와주는 도구이
  - migrations 디렉터리는 alembic 도구를 사용할 때 생성되는 리비전 파일들을 저장하는 용도
  - alembic.ini 파일은 alembic의 환경설정 파일
- $ pip install alembic
- $ alembic init migrations (최초 한번만 수행)
- migrations/env.py, alembic.ini 파일 수정
- models.Base.metadata.create_all(bind=engine)는 테이블을 생성하는 매우 간단한 방법이지만, 
  테이블이 존재하지 않을 때만 생성한다. 따라서, 생성된 테이블의 열을 추가 한다던지 스키마를 업데이트 할 경우 
  아래의 명령을 사용하도록 한다.
  - $ alembic revision --autogenerate
  - $ alembic upgrade head

---
### (3) pydantic
- FastAPI의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용하는 라이브러리
- FastAPI 설치시 함께 설치되기 때문에 따로 설치할 필요는 없다.
- (Pydantic을 이용한) Schema를 사용하는 것은 입출력 값이 정확한지 검증하는 것 외에,
- DB에 저장하는 것과 실제 고객에 응답으로 전달하는 것을 다르게 하기 위함도 있다.

- https://pydantic-docs.helpmanual.io/

---
### (4) Outer-Join
- 예시
  - 질문 데이터가 306개이고
    - db.query(Question).count()
  - 답변 데이터가 7개 일 때
    - db.query(Answer).count()
  - 두 데이터를 Join 하면 7개 데이터를 얻는다.
    - db.query(Question).join(Answer).count()
  - 이는 답변이 달리지 않는 조회되지 않기 때문인데, 이 문제를 해결하기 위해 Outer-Join 을 생각해 볼 수 있다.
    - db.query(Question).outerjoin(Answer).count()
    - 질문에 답변이 두개 이상 달리더라도 모두 조회된다.
    - 조회된 질문	질문에 달린 답변	중복 여부
      - 1	질문 1에 달린 답변1	중복
      - 1	질문 1에 달린 답변2	중복
      - 2	질문 2에 달린 답변1	중복
      - 2	질문 2에 달린 답변2	중복
      - 3	답변 없음	중복 아님
      - …	…	…
      - 306	답변 없음	중복 아님
    - 이때 중복을 제거해야 할 필요가 있다.
      - db.query(Question).outerjoin(Answer).distinct().count

---
### (5) Sub-Query
- 검색 기능을 구현하려면, 답변 내용 뿐만 아니라 답변 작성자도 검색 조건에 포함해야 한다.
- 답변 내용 검색은 Answer 모델을 아우터 조인하면 쉽게 해결되지만,
- 답변 작성자를 조건에 추가하는 것은 쉽지 않다.
- 예시)
```
sub_query = db.query(Answer.question_id, Answer.content, User.username)\
                    .outerjoin(User, Answer.user_id == User.id).subquery()
```
- 이 서브쿼리는 답변 모델과 사용자 모델을 OuterJoin 하여 만든 것으로, Answer.content, User.username가 조회 항목으로 추가됨
- 그리고 이 서브쿼리와 질문 모델을 연결할 수 있는 질문 id에 해당하는 Answer.question_id도 조회 항목에 추가되었다.
- 이처럼 서브쿼리를 사용하면 다음과 같이 Question 모델과 서브쿼리를 OuterJoin할 수 있다.
```
db.query(Question).outerjoin(sub_query, sub_query.c.question_id == Question.id).distinct()
```
- sub_query.c.question_id에 사용한 c는 서브쿼리의 조회 항목을 의미
- 이제 sub_query를 OuterJoin 했으므로 sub_query의 조회 항목을 filter 함수에 조건으로 추가할 수 있다.
```
db.query(Question).outerjoin(sub_query, sub_query.c.question_id == Question.id) \
    .filter(sub_query.c.content.ilike('%파이썬%') |   # 답변내용
           sub_query.c.username.ilike('%파이썬%')    # 답변작성자
           ).distinct()

```
- 검색 코드
```

# 검색
search = '%%{}%%'.format(keyword)
sub_query = db.query(Answer.question_id, Answer.content, User.username)\
    .outerjoin(User, Answer.user_id == User.id).subquery()
question_list = db.query(Question)\
    .outerjoin(User)\
    .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
    .filter(Question.subject.ilike(search) |      # 질문제목
            Question.content.ilike(search) |      # 질문내용
            User.username.ilike(search) |         # 질문작성자
            sub_query.c.content.ilike(search) |   # 답변내용
            sub_query.c.username.ilike(search)    # 답변작성자
            )\
    .distinct()

```
