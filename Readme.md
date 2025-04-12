## FastAPI 서버 실행
* uvicorn main:app --reload


## FrontEnd
- [Svelte](https://svelte.dev/)
  - boilerplate 코드가 적다
  - 앱을 빌드 시점에  Vanilla JavaScript Bundle로 컴파일 하여, html, css, js 파일로 변환해 준다.
  - Node.js 서버를 사용해 로컬에서 실행할 수 있다.

## 파일 구조
```
├── main.py
├── database.py
├── models.py
├── domain
│   ├── answer
│   ├── question
│   └── user
└── frontend
```

## DB 구조
- Question
```
속성명	설명
id	질문 데이터의 고유 번호
subject	질문 제목
content	질문 내용
create_date	질문 작성일시
```

- Answer
```
속성명	설명
id	답변 데이터의 고유 번호
question_id	질문 데이터의 고유 번호(어떤 질문에 달린 답변인지 알아야 하므로 질문 데이터의 고유 번호가 필요하다)
content	답변 내용
create_date	답변 작성일시
```
- 프론트엔드에서 FastAPI 백엔드 서버로 호출이 가능하게 하기 위해 CORS 설정 필요


### TODO  
[] 답변 페이징과 정렬 기능 추가
[] 댓글 기능 추가
[] 카테고리 기능 추가
[] 비밀번호 찾기와 변경
[] 프로필
[] 최근 답변과 최근 댓글
[] 조회 수
[] 소셜 로그인 기능
