FROM python:bullseye

LABEL maintainer="Zakkoree"<zdy.mail@foxmail.com>

LABEL description="Woiden And Hax Auto Extend"

RUN apt update && apt install ffmpeg -y  \
  && apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH="/app:${PATH}"

COPY requirements.txt .

# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m playwright install

RUN playwright install-deps

COPY . .
ENTRYPOINT ["python3","main.py"]
