import os
import numpy as np

from src.core.mic_service import record_chunk

def record_worker(audio_queue, record_stop_event):

    os.makedirs("recordings", exist_ok=True)

    idx = 0

    print("[REC] 녹음중...")

    while not record_stop_event.is_set():

        audio = record_chunk(5)

        if np.max(np.abs(audio)) < 0.03:
            continue

        if record_stop_event.is_set():
            break   

        audio_queue.put(audio)

        idx += 1

