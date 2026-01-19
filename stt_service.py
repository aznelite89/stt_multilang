from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import shutil

app = FastAPI()

model = WhisperModel("small", device="cpu", compute_type="int8")

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
