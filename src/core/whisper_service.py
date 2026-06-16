import time

from faster_whisper import WhisperModel 
  
# =====================================
# Whisper 모델 로딩
# =====================================
# 음성 인식 작업을 수행하는 데 사용됩니다. 
#
# base:
# - tiny보다 정확도 높음
# - small보다 가벼움
# - CPU에서도 무난하게 사용 가능
#
# device="cpu"
# - GPU 없이 CPU 사용
#
# compute_type="int8" 
# - 모델의 가중치를 8비트 정수로 양자화하여 
# - 메모리 사용량 감소
# - CPU 환경에서 속도 향상
#
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio):
    # STT 처리 시간 측정 시작
    start = time.time()

    # =====================================
    # 음성 -> 텍스트 변환
    # =====================================
    #
    # segments
    # - 인식된 문장 조각들
    # - generator : 한 번 순회하면 소진됩니다.
    #
    # _
    # - 부가 정보(언어, 처리시간 등)
    # - 현재 사용하지 않으므로 _

    # beam_size=1 : 빔 서치 알고리즘에서 후보 문장 수를 1로 설정하여 
    # 가장 가능성 높은 문장 하나만 반환
    # 탐색 공간을 줄여서 처리 속도 향상, 정확도는 약간 낮아질 수 있음 

    # initial_prompt : 초기 프롬프트를 통해 모델이 회의록 생성에 적합한 방식으로 인식하도록 유도
    #
    # transcribe는 음성 데이터를 텍스트로 변환하는 함수입니다.
    segments, _ = model.transcribe( 
        audio,     # numpy 배열 형태의 음성 데이터
        language="ko",
        beam_size=1, 
        initial_prompt=""" 
        회의록 자동 생성.
        일정, 개발, 프로젝트 등의 IT관련 용어가 자주 나옵니다.
        """ 
    )
    # =====================================
    # Segment 합치기
    # =====================================
    ## " "로 각 segment.text를 연결하여 하나의 문자열로 만듭니다.
    # 예)
    #
    # segment1.text
    # "안녕하세요"
    #
    # segment2.text
    # "회의를 시작하겠습니다"
    #
    # 결과:
    # "안녕하세요 회의를 시작하겠습니다"
    text = " ".join( 
        segment.text
        for segment in segments
    )

    return text