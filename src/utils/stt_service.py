from queue import Empty

def stt_worker(
    audio_queue,
    transcript_queue,
    record_stop_event,
    speech_to_text
):
    while True:

        try:
            audio = audio_queue.get(timeout=1)

        except Empty:

            if record_stop_event.is_set():
                break

            continue

        try:
            text = speech_to_text(audio)
        except Exception as e:
            print("STT 오류:", e)
            continue
            
        transcript_queue.put(text)
