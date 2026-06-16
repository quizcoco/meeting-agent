import os

from fastapi import FastAPI

from src.rag.embedding.embedder import Embedder
from src.rag.vectorstore.vector_store import VectorStore
from src.rag.ask_service import AskService
from src.services.meeting_service import create_meeting

from src.api.schemas import AskRequest, MeetingRequest
from src.services.s3_service import (
    exists_vector_store,
    download_vector_store
)


app = FastAPI()


embedder = Embedder()


if not os.path.exists("vector_store/index.faiss"):

    if exists_vector_store():
        print("S3에서 Vector Store 다운로드")
        download_vector_store()
    else:
        print("S3에 Vector Store 없음. 새로 생성합니다.")
vector_store = VectorStore()

ask_service = AskService(
    embedder,
    vector_store
)



@app.get("/")
def health_check():
    return {
        "message": "AI Meeting Agent API"
    }


@app.post("/ask")
def ask(request: AskRequest):

    answer = ask_service.ask(request.query)

    return {
        "answer": answer
    }

@app.post("/meeting")
def create_meeting_api(request: MeetingRequest):

    result = create_meeting(
        request.text,
        embedder,
        vector_store
    )

    return {
        "message": "회의록 생성 완료",
        "result": result
    }