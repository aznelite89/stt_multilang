FROM python:3.11-slim

# Install ffmpeg for decoding webm/opus/mp3
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["sh", "-c", "uvicorn stt_service:app --host 0.0.0.0 --port 9000"]
