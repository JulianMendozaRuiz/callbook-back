from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.routers.transcription import router as transcription_router
from app.routers.videocall import router as videocall_router

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videocall_router)
app.include_router(transcription_router)


@app.get("/")
def root():
    return Response("Server is running!", media_type="text/plain")
