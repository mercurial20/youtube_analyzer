from fastapi import FastAPI
from gemini_client import summarize_long_text
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_utils import extract_youtube_id

app = FastAPI()
ytt_api = YouTubeTranscriptApi()

origins = [
    "http://localhost:5173",   # Vite dev server
    "http://127.0.0.1:5173",
    # сюда потом можно добавить прод-урлы фронта
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # или ["*"] для вообще всех
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST и т.д.
    allow_headers=["*"],            # Authorization, Content-Type и т.п.
)


@app.get("/video/transcript")
def get_transcript(url: str):
    videoId = extract_youtube_id(url)
    if not videoId:
        raise HTTPException(
            status_code=400,
            detail="URL is incorrect. Try another one. URL неправилный, попробуйте другой или скопируйте с браузера",
        )
    try:
        fetched = ytt_api.fetch(
            videoId,
            languages=["ru", "en"],  # приоритет языков
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cannot fetch transcript: {e}")

    raw_items = fetched.to_raw_data()
    if not raw_items:
        raise HTTPException(status_code=404, detail="Transcript not found")

    full_text = " ".join(item["text"] for item in raw_items)
    try:
        summary = summarize_long_text(full_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    return {
        "video_id": videoId,
        "original_length_chars": len(full_text),
        "summary": summary,
    }

