from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

import models
from database import engine

#
# # Base 클래스를 상속받은 모든 클래스를 데이터베이스에 생성
# # 데이터베이스에 테이블이 존재하지 않을 경우에만 테이블을 생성
models.Base.metadata.create_all(bind=engine) # FastAPI 실행시 필요한 테이블들이 모두 생성된다.

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/hello")
# def hello():
#     return {"message": "Hello World"}

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")