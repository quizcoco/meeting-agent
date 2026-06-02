from queue import Empty

def stt_worker(
    audio_queue,
    transcript_queue,
    record_stop_event,
    speech_to_text
):
    print("STT Thread 시작")
    while True:

        # print("1. queue 대기")

        try:
            audio = audio_queue.get(timeout=1)

            print("2. queue 수신")

        except Empty:

            if record_stop_event.is_set():
                break

            continue

        print("3. STT 시작")

        try:
            text = speech_to_text(audio)
        except Exception as e:
            print("STT 오류:", e)
            continue
            
        print("4. STT 완료")

        transcript_queue.put(text)

        print("5. transcript 저장")
