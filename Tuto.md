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
- $ alembic init alembic
- migrations/env.py, alembic.ini 파일 수정

---
### (3) pydantic
- FastAPI의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용하는 라이브러리
- FastAPI 설치시 함께 설치되기 때문에 따로 설치할 필요는 없다.
- (Pydantic을 이용한) Schema를 사용하는 것은 입출력 값이 정확한지 검증하는 것 외에,
- DB에 저장하는 것과 실제 고객에 응답으로 전달하는 것을 다르게 하기 위함도 있다.

- https://pydantic-docs.helpmanual.io/