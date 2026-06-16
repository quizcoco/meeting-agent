def validate_minutes_schema(minutes):

    required_fields = [
        "title",
        "purpose",
        "discussion",
        "decision",
        "action_items",
        "summary"
    ]

    # 필수 필드 존재 여부
    for field in required_fields:

        if field not in minutes:
            raise ValueError(
                f"필수 필드 누락: {field}"
            )

    # 문자열 필드 검증
    text_fields = [
        "title",
        "purpose",
        "discussion",
        "decision",
        "summary"
    ]

    for field in text_fields:

        if not isinstance(minutes[field], str):
            raise ValueError(
                f"{field} 타입 오류"
            )

        if not minutes[field].strip():
            raise ValueError(
                f"{field} 비어있음"
            )

    # action_items 검증
    if not isinstance(
        minutes["action_items"],
        list
    ):
        raise ValueError(
            "action_items 타입 오류"
        )

    return True


def validate_minutes_content(minutes):

    if not minutes["title"].strip():
        raise ValueError("title 비어있음")

    if not minutes["summary"].strip():
        raise ValueError("summary 비어있음")

    return True

def validate_minutes(minutes):

    validate_minutes_schema(minutes)

    validate_minutes_content(minutes)

    return True