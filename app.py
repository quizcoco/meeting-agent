from src.rag.ask_service import AskService
from src.core.recorder_service import record_meeting
from src.services.meeting_service import create_meeting

from src.rag.embedding.embedder import Embedder
from src.rag.vectorstore.vector_store import VectorStore

embedder = Embedder()
vector_store = VectorStore()
ask_service = AskService(embedder, vector_store)

# stt, 회의 텍스트 누적
meeting_text = record_meeting()

# 회의록 생성 (전체 회의 내용 -> LLM 요약 -> 회의록) 벡터 저장까지
create_meeting(meeting_text, embedder, vector_store)


# 검색, 도구사용, 에이전트
user_query = input("질문 : ")
answer = ask_service.ask(user_query)

print(answer)
