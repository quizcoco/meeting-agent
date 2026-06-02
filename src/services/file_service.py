from datetime import datetime
import os


def save_minutes(content):

    os.makedirs("minutes", exist_ok=True)

    filename = datetime.now().strftime(
        "%Y%m%d_%H%M%S.md"
    )

    path = os.path.join(
        "minutes",
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    print(f"회의록 저장 완료: {path}")

def save_raw_text(content):

    os.makedirs("minutes", exist_ok=True)

    filename = datetime.now().strftime(
        "%Y%m%d_%H%M%S_raw.txt"
    )

    path = os.path.join(
        "minutes",
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    print(f"원본 저장 완료: {path}")