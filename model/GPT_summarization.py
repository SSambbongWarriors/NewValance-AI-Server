import json
import re
import os
import sys
import subprocess
from openai import OpenAI



# def install():
#     package = "openai"

#     subprocess.check_call([sys.executable, "pip", "install", package])

def GPT(total_news):


# Set your OpenAI API key

    OPENAI_API_KEY = ("")

    client = OpenAI(
        api_key = OPENAI_API_KEY
    )

    summerize_formal = ""
    summerize_casual = ""
    summerize_TTV = []

    # Define the system role and model
    model = 'gpt-4o'
    system_role = ("당신은 뉴스 전문가로, 기사를 요약하여 요청받은 말투로 두 개의 대본을 생성한다.\n"
                    "응답은 두 개의 문자열 리스트를 담은 하나의 파이썬 리스트 형식이어야 한다.")

    # Sample article and query
    

    # Prepare the prompt
    query = total_news[0] + " 다음 기사를 한 문장 당 약 60자 정도 되는 다섯 개의 문장으로 요약해서 두 개의 문자열 배열로 리턴해줘. 첫번째 배열은 아나운서처럼 -입니다 체의 말투고 두 번째 배열은 친근하고 장난스러운 말투여야 해. 그리고 두 개의 내용은 동일하되 말투만 달라야 해."

    # Define the messages
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": query}
    ]

    # Make the request to the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    # Print the response
    answer = response.choices[0].message.content
    print(answer)

    # 파이썬 코드 블록 제거
    cleaned_response = re.sub(r'```python\n|\n```', '', answer)

    try:
        parsed_answer = json.loads(cleaned_response)
    except json.JSONDecodeError:
        print("JSON 파싱 오류. API 응답:", cleaned_response)
        parsed_answer = []

    # 파싱된 결과 확인
    if isinstance(parsed_answer, list) and len(parsed_answer) == 2:
        summerize_formal = parsed_answer[0]
        summerize_casual = parsed_answer[1]
        print("Formal summary:", summerize_formal)
        print("Casual summary:", summerize_casual)
    else:
        print("예상치 못한 응답 형식:", parsed_answer)

    # Define the system role and model
    system_role_2 = (
                "You are a content generator for a text-to-video application. Your task is to create dynamic "
                    "and simple English sentences that describe a scene. Each sentence must:\n"
                    "- Contain a subject (e.g., a person, an object, or an animal).\n"
                    "- If the subject is a human, specify whether it is 'a man' or 'a woman.'\n"
                    "- Optionally describe the clothing they are wearing (e.g., 'a man in a blue shirt').\n"
                    "- Include a verb that describes an action or movement in simple and common terms.\n"
                    "- Avoid abstract verbs or phrases like 'say we need,' 'think about,' 'discuss the need,' and replace them with visible actions (e.g., 'write a note,' 'stand in a meeting room').\n"
                    "- Avoid sentences that cannot be easily visualized in a video (e.g., 'More people say we need an investigation.').\n"
                    "- Provide a background context where the subject is located (e.g., 'on the street,' 'in the park,' 'at a school').\n"
                    "Use only common words suitable for beginners or children learning English.\n"
                    "\nExample sentences:\n"
                    "- A man runs on the street.\n"
                    "- A dog jumps in the park.\n"
                    "- A teacher talks in a classroom."
                    "\nReturn all generated sentences as a single array of strings, where each sentence is an element of the array.\n"
                    "\nExample:\n"
                    "Input: 'The president announced new measures to improve education, including increased funding and teacher training programs.'\n"
                    "Output: [\"A man in a suit talks in a big hall.\", \"A woman writes notes in a classroom.\", \"Students read books in a library.\"]"
                )

    # Prepare the prompt
    query_2 = str(summerize_formal)

    # Define the messages
    messages_2 = [
        {"role": "system", "content": system_role_2},
        {"role": "user", "content": query_2}
    ]

    # Make the request to the OpenAI API
    response_2 = client.chat.completions.create(
        model=model,
        messages=messages_2,
    )

    # Print the response
    answer_2 = response_2.choices[0].message.content
    print(answer_2)

    # 파이썬 코드 블록 제거
    cleaned_response = re.sub(r'```python\n|\n```', '', answer_2)

    try:
        parsed_answer = json.loads(cleaned_response)
    except json.JSONDecodeError:
        print("JSON 파싱 오류. API 응답:", cleaned_response)
        parsed_answer = []

    # 파싱된 결과 확인
    if isinstance(parsed_answer, list) and len(parsed_answer) == 5:
        summerize_TTV = parsed_answer
        print("summerize_TTV:", summerize_TTV)
    else:
        print("예상치 못한 응답 형식:", parsed_answer)


    sum=[summerize_casual, summerize_formal, summerize_TTV]

    return sum

'''
def fullSummarize(total_news):

    sum=GPT(total_news)

    sum = [summerize_casual, summerize_formal, summerize_TTV]

    return sum
'''

if __name__=="__main__":

    #install()
    sum=GPT(total_news)
