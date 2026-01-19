Speech to text service with multi languages supported

## create virtual env for python

# source venv/bin/activate

# --------------------------------------------------#

## install those deps

# pip install fastapi uvicorn faster-whisper

# --------------------------------------------------#

## to run it locally

# uvicorn stt_service:app --host 0.0.0.0 --port 9000

# docs: http://127.0.0.1:9000/docs#/

# --------------------------------------------------#

### LOCAL DOCKER BUILD & RUN

## BUILD

# docker build -t stt-local .

## RUN

# docker run --rm -p 9000:9000 stt-local

## Test in browser:-

# http://127.0.0.1:9000/docs

# --------------------------------------------------#

### REBUILD WHEN U HAVE CHANGE when using local Dockerfile img

# docker build -t stt-local .

# docker stop stt-local 2>/dev/null

# docker rm stt-local 2>/dev/null

# docker run -d --restart unless-stopped -p 9000:9000 --name stt-local stt-local

# --------------------------------------------------#
