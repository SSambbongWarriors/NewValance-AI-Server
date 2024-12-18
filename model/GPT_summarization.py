import json
import re
import os
import sys
import subprocess
from openai import OpenAI


# openai key를 위한 디렉토리 경로 설정
current_dir = os.path.dirname(os.path.abspath("/home/elicer/capstone_1216/model/GPT_summarization.py"))
key_dir = os.path.join(current_dir, "../key")

# key 디렉토리를 Python 경로에 추가
sys.path.append(key_dir)

# get_key 함수 import
from key_manager import get_key


def GPT(article):
    # Set your OpenAI API key
    OPENAI_API_KEY = get_OPENAI_key()
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    summerize_formal = ""
    summerize_casual = ""
    summerize_TTV = ""

    # Define the system role and model
    model = 'gpt-4o'
    system_role_clean = (
        "당신은 데이터를 정제하는 일을 수행합니다.\n"
        "입력으로 들어오는 데이터는 뉴스 기사를 크롤링한 문자열 배열 데이터입니다.\n"
        "배열에 포함된 문자열 중 뉴스 내용과 관련없는 출처나 저작권 정보, 기자 정보와 같은 내용을 포함한 문자열은 삭제해야 합니다.\n"
        "문자열의 내용을 수정해서는 안되며 삭제만 가능합니다.\n"
        "결과는 하나의 문자열로 리턴합니다."
    )

    # Prepare the prompt
    query_clean = str(article)

    # Define the messages
    messages_clean = [
        {"role": "system", "content": system_role_clean},
        {"role": "user", "content": query_clean}
    ]

    response_clean = client.chat.completions.create(
        model=model,
        messages=messages_clean,
    )

    answer_clean = response_clean.choices[0].message.content

    # 뉴스 요약 텍스트 생성
    system_role_summerize = (
        "당신은 뉴스 전문가로, 기사를 한 문장 당 약 60자 정도 되는 다섯 개의 문장으로 요약한다.\n"
        "첫 번째 문자열 리스트는 아나운서처럼 -입니다 체의 말투로 요약된 다섯 개의 문장이다.\n"
        "두 번째 문자열 리스트는 친근하고 장난스러운 말투로 요약된 다섯 개의 문장이다.\n"
    )

    query_summerize = str(answer_clean)

    messages_summerize = [
        {"role": "system", "content": system_role_summerize},
        {"role": "user", "content": query_summerize}
    ]

    response_summerize = client.chat.completions.create(
        model=model,
        messages=messages_summerize,
    )

    answer = response_summerize.choices[0].message.content

    cleaned_response = re.sub(r'```python\n|\n```', '', answer)

    try:
        parsed_answer = json.loads(cleaned_response)
        if isinstance(parsed_answer, list) and len(parsed_answer) == 2:
            summerize_formal = parsed_answer[0]
            summerize_casual = parsed_answer[1]
    except json.JSONDecodeError:
        print("JSON 파싱 오류. API 응답:", cleaned_response)

    # Define the system role for TTV
    system_role_TTV = (
        "You are a content generator for a text-to-video application. Your task is to create dynamic "
        "and simple English sentences that describe a scene. Each sentence must:\n"
        "- Contain a clear subject (e.g., a person, an object, or an animal).\n"
        "- Include a verb that describes an action or movement in simple and common terms.\n"
        "- Return all generated sentences as a single array of strings.\n"
    )

    query_TTV = str(summerize_formal)

    messages_TTV = [
        {"role": "system", "content": system_role_TTV},
        {"role": "user", "content": query_TTV}
    ]

    response_TTV = client.chat.completions.create(
        model=model,
        messages=messages_TTV,
    )

    answer_TTV = response_TTV.choices[0].message.content

    try:
        cleaned_response = re.sub(r'```python\n|\n```', '', answer_TTV)
        parsed_answer = json.loads(cleaned_response)
        if isinstance(parsed_answer, list) and len(parsed_answer) == 5:
            summerize_TTV = parsed_answer
        else:
            print("API 응답 형식이 예상과 다릅니다.")
            summerize_TTV = ["A scene description is unavailable."] * 5
    except json.JSONDecodeError:
        print("JSON 파싱 오류. API 응답:", cleaned_response)
        summerize_TTV = ["A scene description is unavailable."] * 5

    return [summerize_casual, summerize_formal, summerize_TTV]


if __name__ == "__main__":
    summaries = GPT(example_article)
    print("Final Summaries:", summaries)
