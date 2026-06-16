from queue import Empty, Queue
from threading import Thread
import threading # 여러 작업을 동시에 실행하기 위해 사용

from core.recording_worker import record_worker
from src.utils.stt_service import stt_worker
from src.core.whisper_service import speech_to_text


# =====================================
# Queue
# =====================================
#
# 스레드 간 데이터를 안전하게 주고받기 위한 자료구조
#
# audio_queue
# : 녹음 스레드 -> STT 스레드
#
# transcript_queue
# : STT 스레드 -> 메인 스레드
#
# =====================================
# Event
# =====================================
#
# 스레드 종료 신호 전달용
#
# set()   -> 종료 요청
# is_set()-> 종료 여부 확인
#

def wait_for_exit(record_stop_event):

    while True:

        cmd = input()

        if cmd.strip() == r"\q":

            print("종료 요청")

            record_stop_event.set()
            break


def record_meeting():

    # 스레드 간 통신용 Queue
    # 녹음 데이터 저장
    audio_queue = Queue()
    # 변환된 텍스트 저장
    transcript_queue = Queue()

    # 녹음 종료 요청 이벤트
    record_stop_event = threading.Event()

    # 프로그램 종료 요청
    program_stop_event = threading.Event()

    # 전체 회의 내용 저장
    meeting_text = ""

    # =====================================
    # 녹음 스레드 생성
    # 역할:
    # 마이크 -> audio_queue
    record_thread = Thread(
        target=record_worker,
        args=(
            audio_queue,
            record_stop_event
        )
    )
    # STT 스레드 생성
    # =====================================
    #
    # 역할:
    #
    # audio_queue
    #      ↓
    # speech_to_text()
    #      ↓
    # transcript_queue

    stt_thread = Thread(
        target=stt_worker,
        args=(
            audio_queue,
            transcript_queue,
            record_stop_event,
            speech_to_text
        )
    )

    # 스레드 시작
    record_thread.start()
    stt_thread.start()

    # =====================================
    # 엔터 입력 감지 스레드
    # =====================================
    #
    # daemon=True
    #
    # 메인 프로그램 종료 시
    # 자동 종료됨
    exit_thread = Thread(
        target=wait_for_exit,
        args=(record_stop_event,),
        daemon=True
    )

    exit_thread.start()

    print("회의 시작")
    print(r"종료하려면 \q를 누르세요.")

    # =====================================
    # 메인 루프
    # =====================================
    #
    # transcript_queue에서
    # STT 결과를 계속 가져온다.

    while True:

        try:
            # 1초 동안 대기
            #
            # 텍스트가 들어오면 반환
            # 없으면 Empty 발생
            text = transcript_queue.get(timeout=1)

            print()
            print("==========")
            print(text)
            print("==========")

            # 회의 전체 내용 누적
            meeting_text += text + "\n"

        except Empty:
            # =====================================
            # 종료 조건
            # =====================================
            #
            # 1. 사용자가 종료 요청했고
            # 2. STT 결과도 더 이상 없고
            # 3. 음성 데이터도 더 이상 없으면
            #
            # 완전 종료
            #
            if (
                    record_stop_event.is_set()
                    and transcript_queue.empty()
                    and audio_queue.empty()
                ):
                    break   
            
    # =====================================
    # 스레드 종료 대기
    # =====================================
    #
    # join()
    #
    # 해당 스레드가 완전히 종료될 때까지
    # 현재 스레드를 멈춘다.

    # record_thread와 stt_thread가 종료될 때까지 기다립니다.
    record_thread.join()
    stt_thread.join()

    print()
    print("system: 회의 종료")
    print()

    return meeting_text