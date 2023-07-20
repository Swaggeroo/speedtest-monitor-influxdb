FROM python:3
LABEL authors="Swaggeroo"

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    apt-transport-https \
    gnupg1 \
    dirmngr \
    lsb-release \
    && apt-get clean

RUN curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash

RUN apt-get install -y speedtest

COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD [ "python", "./main.py"]