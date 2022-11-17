FROM python:bullseye

ARG CHROME_VERSION="101.0.4951.54-1"
# Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
RUN apt update && apt install unzip wget ffmpeg -y  \
  && wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb \
  && apt clean && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN wget  --no-verbose  https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip\
    && rm chromedriver_linux64.zip


ENV PATH="/app:${PATH}"

COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python3","main.py"]
