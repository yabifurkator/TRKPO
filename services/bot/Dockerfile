# FROM python:3.10-bullseye
FROM selenium/standalone-chrome

# for selenium

## google-chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y --fix-missing google-chrome-stable

## chrome driver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# ENV DISPLAY=:99

RUN sudo apt update
RUN sudo apt install -y python3-pip

COPY . /app

RUN [ "sudo", "pip3", "install", "--requirement", "/app/requirements.txt" ]

EXPOSE 8989

# ENTRYPOINT [ "python", "/app/src/main.py"]
ENTRYPOINT [ "./app/start.sh" ]
