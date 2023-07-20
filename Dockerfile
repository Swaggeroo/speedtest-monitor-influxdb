FROM ubuntu:latest
LABEL authors="frede"

ENTRYPOINT ["top", "-b"]