FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && \
pip install --no-cache-dir -r /app/requirements.txt
