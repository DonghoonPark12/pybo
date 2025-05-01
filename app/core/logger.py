import logging
import os

# 로그 레벨 설정
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# 로거 설정
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # 콘솔 출력
    ],
)

# 로거 인스턴스 생성
logger = logging.getLogger("app")