from src.config.settings import SUMMARY_LAMBDA_NAME
from src.services.context_service import build_document
from src.services.lambda_service import invoke_lambda
from src.utils.parse_service import parse_claude_json
from src.services.validation_service import validate_minutes
from src.rag.ingestion.index import index_meeting
from src.repository.rds_repository import save_minutes





def create_meeting(meeting_text, embedder, vector_store):


    result = invoke_lambda({"text": meeting_text}, SUMMARY_LAMBDA_NAME) # Lambda로 회의록 생성 요청
    document = "" # Vector Store 저장용 문서
    try:
        # Lambda에서 반환된 JSON 문자열을 파싱하여 딕셔너리로 변환
        meeting_json = parse_claude_json(result)

        validate_minutes(meeting_json)

        meeting_id = save_minutes(
            meeting_text,
            meeting_json
        )   

        # 벡터화 및 Vector Store 저장을 위해 전체 회의록 텍스트 대신 요약문을 사용
        document = build_document(
            meeting_json
        )

        # 벡터에 저장
        index_meeting(
            meeting_id,
            document,
            embedder, 
            vector_store
        )
        
    except Exception as e:

        print(
            f"회의록 저장 실패: {e}"
        )


    # Producer → Queue → Consumer 패턴
    # - Producer: 데이터를 생성하여 Queue에 넣는 역할
    # - Consumer: Queue에서 데이터를 꺼내 처리하는 역할
    # 녹음과 STT를 분리하기 위해 Queue 기반 Producer-Consumer 구조를 사용

    # record_thread
    #       ↓
    #   audio_queue
    #       ↓
    #    stt_thread
    #       ↓
    # transcript_queue
    #       ↓
    #    main thread
    #       ↓
    #  create_minutes()
    #       ↓
    #  save_minutes()
