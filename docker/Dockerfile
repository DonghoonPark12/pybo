FROM python:3.9

RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN apt-get update --allow-releaseinfo-change && \
    apt-get install --no-install-recommends -y \
    python3-pip python3-setuptools python3-wheel vim tar locales build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

# locale 설정
#RUN locale-gen ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR:ko
ENV LC_ALL=ko_KR.UTF-8

# timezone 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# timezone 설정
CMD ["uvicorn", "app.main:app", "--port", "8000", "--reload"]
