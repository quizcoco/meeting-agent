
def build_document(meeting_json):
    # Vector Store에 저장할 문서를 만든다.
    return f"""
제목:
{meeting_json["title"]}

목적:
{meeting_json["purpose"]}

논의:
{meeting_json["discussion"]}

결정:
{meeting_json["decision"]}

요약:
{meeting_json["summary"]}
"""


def build_context(meetings):

    contexts = []

    for meeting in meetings:

        contexts.append(
            f"""
회의ID: {meeting["id"]}

제목:
{meeting["title"]}

요약:
{meeting["summary"]}

목적:
{meeting["purpose"]}

논의:
{meeting["discussion"]}

결정:
{meeting["decision"]}

액션아이템:
{meeting["action_items"]}

생성일:
{meeting["created_at"]}

"""
        )

    return "\n\n".join(contexts)

