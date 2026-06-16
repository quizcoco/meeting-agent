
import json


def parse_claude_json(result):

    result = result.strip()

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()
    try:
        return json.loads(result) 

    except:
        json_text = extract_json(result)
        return json.loads(json_text)

def extract_json(text):

    stack = []
    json_start = None

    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                json_start = i
            stack.append(char)
        elif char == '}' and stack:
            stack.pop()
            if not stack and json_start is not None:
                return text[json_start:i+1]

    raise ValueError("유효한 JSON을 찾을 수 없습니다.")