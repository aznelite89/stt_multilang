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

    model = WhisperModel("base", device="cpu", compute_type="int8")

    @app.post("/transcribe")
    async def transcribe(file: UploadFile = File(...)):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        segments, info = model.transcribe(tmp_path, vad_filter=False, beam_size=2, best_of=2, temperature=0.0)

        text = "".join(seg.text for seg in segments)

        return {
            "language": info.language,
            "probability": info.language_probability,
            "text": text
        }

    @app.get("/")
    def health():
        return {"status": "STT Whisper MultiLang running"}
