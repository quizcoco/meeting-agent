import os
from openai import OpenAI

from dotenv import load_dotenv
# import google.generativeai as genai

load_dotenv()

# 제미나이
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-2.5-flash")

# GROQ
client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url=os.getenv("BASE_URL")
        )

def create_minutes(text):

    prompt = f"""
    다음 회의 내용을 분석하여

    1. 회의 제목
    2. 참석자
    3. 주요 안건
    4. 결정 사항
    5. TODO

    형식으로 작성하시오.

    회의내용:
    {text}
    """
    # 제미나이
    # response = model.generate_content(prompt)
    # print(response.text)

    # return response.text

    # GROQ
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    return response.choices[0].message.content