import os
import wave
import numpy as np

from src.core.mic_service import record_chunk

def record_worker(audio_queue, record_stop_event):

    os.makedirs("recordings", exist_ok=True)

    idx = 0

    while not record_stop_event.is_set():

        print(f"[REC] {idx} 녹음중...")

        audio = record_chunk(5)

        if np.max(np.abs(audio)) < 0.03:
            print("침묵 건너뜀")
            continue

        if record_stop_event.is_set():
            break   

        audio_queue.put(audio)
        print("queue:", audio_queue.qsize())

        idx += 1


def clear_recordings():

    os.makedirs("recordings", exist_ok=True)

    for file in os.listdir("recordings"):

        path = os.path.join("recordings", file)

        if os.path.isfile(path):
            os.remove(path)