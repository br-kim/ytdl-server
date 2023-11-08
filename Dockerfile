FROM arm64v8/python:3.10-alpine


WORKDIR /app/app

COPY . /app


RUN pip install -r requirements.txt
RUN apk add ffmpeg
RUN mkdir download
