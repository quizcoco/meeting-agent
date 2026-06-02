import json
import os
import re
from urllib import response

from openai import OpenAI

# import google.generativeai as genai

# 제미나이
# model = genai.GenerativeModel("gemini-2.5-flash")

# GROQ
model = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url=os.getenv("BASE_URL")
        )

def validate_minutes(transcript, minutes):

    prompt = f"""
    원본 회의 내용

    {transcript}

    -----------------

    생성된 회의록

    {minutes}

    -----------------

    아래를 검증하시오.

    1. 회의록에 없는 내용이 추가되었는가(참석자 정보 제외)
    2. 중요한 TODO가 누락되었는가
    

    정상인 경우

    {{"status":"PASS"}}

    문제가 있는 경우

    {{"status":"FAIL","reason":"설명"}}

    ```json은 제외하고, JSON형태로 출력하시오. 

    """

    # response = model.generate_content(prompt)
    response = model.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]   )
    print(response.choices[0].message.content)

    text = response.choices[0].message.content.strip()
    # text = response.text.strip() # 제미나이의 경우 .text로 결과를 가져옴

    match = re.search(r'\{.*\}', text, re.DOTALL)

    if match:
        result = json.loads(match.group())
    else:
        print("JSON 파싱 실패")
        result = {"status": "FAIL", "reason": "JSON 파싱 실패"}

    return result
