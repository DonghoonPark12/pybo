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

### 사용 서버
- AWS lightsail: 3.38.23.193
- UTC to KTS
  - sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
- 접속
  - Aws ssh -i ./my_thought.pem ubuntu@3.38.23.193
- 실행
  - git clone https://github.com/DonghoonPark12/pybo.git
  - python3 -m .venv my_thought
  - sudo apt install python3-venv
  - sudo apt install alembic
- DB 설정
  - 직접 설치
    - $ sudo apt-get install mysql-server
    - $ sudo ufw allow mysql
    - $ sudo mysql
    - $ ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'XXXX';
    - $ CREATE DATABASE pybo;
    - $ FLUSH PRIVILEGES;
  - 도커로 설정
    - docker run --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=XXXXXX -d mysql:8
    - 


### TODO  
[] 도커 이미지로 ubuntu에서 실행시키기
  - [O] mysql 도커 세팅. 
  - [O] Dockerfile 작성
  - [] CICD 적용. 
  - [] WebSocker 적용. 
 
[] 답변 페이징과 정렬 기능 추가
[] 댓글 기능 추가
[] 카테고리 기능 추가
[] 비밀번호 찾기와 변경
[] 프로필
[] 최근 답변과 최근 댓글
[] 조회 수
[] 소셜 로그인 기능

### Try & Error
- AWS ubuntu 이미지에는 mariadb가 기본적으로 깔려 있나 보다. my-sql 실행시 에러가 생긴다.
```
sudo apt autoremove --purge mysql-server\* mariadb-server\*
sudo rm -rf /var/lib/mysql
sudo rm -rf /etc/mysql/
sudo mkdir -p /etc/mysql/conf.d
sudo apt install mysql-server
```
- 참조: https://stackoverflow.com/questions/70813122/getting-error-mysql-service-failed-because-the-control-process-exited-with-erro
- 메모리가 부족할 경우
```
스왑 공간 추가/확장:
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

영구적으로 적용하려면 /etc/fstab에 추가:
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```