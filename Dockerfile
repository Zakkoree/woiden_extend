FROM python:bullseye

RUN apt update && apt install --assume-yes -y ffmpeg build-essential libssl-dev libffi-dev python-dev  \
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
