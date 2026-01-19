# source venv/bin/activate
# pip install fastapi uvicorn faster-whisper
# uvicorn stt_service:app --host 0.0.0.0 --port 9000
# docs: http://127.0.0.1:9000/docs#/
from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil

app = FastAPI()

# CORS (TODO: later restrict to app domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = WhisperModel("tiny", device="cpu", compute_type="int8")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path, vad_filter=True)

    text = "".join(seg.text for seg in segments)

    return {
        "language": info.language,
        "probability": info.language_probability,
        "text": text,
        "segments": [
            {"start": s.start, "end": s.end, "text": s.text}
            for s in segments
        ]
    }

@app.get("/")
def health():
    return {"status": "STT Whisper MultiLang running"}
