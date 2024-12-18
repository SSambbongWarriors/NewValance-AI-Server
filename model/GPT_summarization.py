import json
import re
import os
import sys
import subprocess
from openai import OpenAI


#openai key를 위한 디렉토리 경로 설정
current_dir = os.path.dirname(os.path.abspath("/home/elicer/capstone_1216/model/GPT_summarization.py"))
key_dir = os.path.join(current_dir, "../key")

# key 디렉토리를 Python 경로에 추가
sys.path.append(key_dir)

# get_key 함수 import
from key_manager import get_OPENAI_key




# def install():
#     package = "openai"

#     subprocess.check_call([sys.executable, "pip", "install", package])

def GPT(article):


# Set your OpenAI API key

    OPENAI_API_KEY = get_OPENAI_key(key="OPENAI_KEY")
    client = OpenAI(
        api_key = OPENAI_API_KEY
    )

    summerize_formal = ""
    summerize_casual = ""
    summerize_TTV = ""

    # Define the system role and model
    model = 'gpt-4o'
    system_role_clean = (
        "당신은 데이터를 정제하는 일을 수행합니다.\n"
        "입력으로 들어오는 데이터는 뉴스 기사를 크롤링한 문자열 배열 데이터입니다.\n"
        "배열에 포함된 문자열 중 뉴스 내용과 관련없는 출처나 저작권 정보, 기자 정보와 같은 내용을 포함한 문자열은 삭제해야합니다.\n"
        "~기자입니다. ㅇㅇ뉴스 ㅇㅇ입니다. 같은 내용의 문자열도 삭제합니다."
        "문자열의 내용을 수정해서는 안되며 삭제만 가능합니다.\n"
        "내용과 관련없는 문자열을 삭제한 뒤에는 모든 문자열을 하나의 문자열로 병합합니다.\n"
        "결과는 하나의 문자열로 리턴합니다."
    )
    # Sample article and query
    

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

    print(answer_clean)

    # 뉴스 요약 텍스트 생성
    system_role_summerize = (
        "당신은 뉴스 전문가로, 기사를 한 문장 당 약 60자 정도 되는 다섯 개의 문장으로 요약한다.\n"
        "만약 기사가 다섯 개의 문장이라면 문장의 길이를 약 60자 정도 되도록 만들고, 다섯개 미만의 문장이라면 다섯 개의 문장으로 만든다.\n"
        "응답은 두 개의 문자열 리스트를 담은 하나의 파이썬 리스트이다.\n"
        "첫 번째 문자열 리스트는 아나운서처럼 -입니다 체의 말투로 요약된 다섯 개의 문장이다.\n"
        "두 번째 문자열 리스트는 친근하고 장난스러운 말투로 요약된 다섯 개의 문장이다.\n"
        "두 문자열 리스트의 내용은 동일해야 하며 말투만 달라야 한다.\n"
        "최종 결과는 두 개의 문자열 리스트를 담은 하나의 파이썬 리스트여야 한다.\n"
    )

    # 정제된 기사 크롤링 자료
    articles = answer_clean


    # user content에 입력할 문자열
    query_summerize = str(articles)

    # 메시지 정의
    messages_summerize = [
        {"role": "system", "content": system_role_summerize},
        {"role": "user", "content": query_summerize}
    ]

    # api 응답 요청
    response_summerize = client.chat.completions.create(
        model=model,
        messages=messages_summerize,
    )

    # 응답 추출
    answer = response_summerize.choices[0].message.content
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
    system_role_TTV = (
                    "You are a content generator for a text-to-video application. Your task is to create dynamic "
                    "and simple English sentences that describe a scene. Each sentence must:\n"
                    "- Contain a clear subject (e.g., a person, an object, or an animal).\n"
                    "- If the subject is a human and not a child, select 'a man' or 'a woman' based on the context of the text.\n"
                    "- Optionally describe the clothing they are wearing (e.g., 'a man in a blue shirt').\n"
                    "- Ensure that each sentence describes no more than two people. Do not include more than two individuals in a single sentence."
                    "- Include a verb that describes an action or movement in simple and common terms.\n"
                    "- Avoid abstract verbs or phrases like 'say we need,' 'think about,' 'discuss the need,' and replace them with visible actions (e.g., 'write a note,' 'stand in a meeting room').\n"
                    "- Avoid sentences that cannot be easily visualized in a video (e.g., 'More people say we need an investigation.').\n"
                    "- You must provide a background context where the subject is located (e.g., 'on the street,' 'in the park,' 'at a school').\n"
                    "- Do not use any proper nouns (e.g., names of people, places, or specific organizations). Instead, use general terms"
                    "Use only common words suitable for beginners or children learning English.\n"
                    "\nExample sentences:\n"
                    "- A man runs on the street.\n"
                    "- A dog jumps in the park.\n"
                    "- Please ensure you return 5 sentences describing a scene.\n"
                    "\nReturn all generated sentences as a single array of strings, where each sentence is an element of the array.\n"
                    "\nExample:\n"
                    "Input: 'The president announced new measures to improve education, including increased funding and teacher training programs.'\n"
                    "Output: [\"A man in a suit talks in a big hall.\", \"A woman writes notes in a classroom.\", \"a kid read books in a library.\"]"
                )

    system_role_TTI = (
                    "You are a content generator for a text-to-video application. Your task is to create dynamic "
                    "and simple English sentences that describe a scene. Each sentence must:\n"
                    "- Contain a clear subject (e.g., a person, an object, or an animal).\n"
                    "- Include a verb that describes an action or movement in simple and common terms.\n"
                    "- Avoid abstract verbs or phrases like 'say we need,' 'think about,' 'discuss the need,' and replace them with visible actions (e.g., 'write a note,' 'stand in a meeting room').\n"
                    "- Avoid sentences that cannot be easily visualized in a video (e.g., 'More people say we need an investigation.').\n"
                    "- You must provide a background context where the subject is located (e.g., 'on the street,' 'in the park,' 'at a school').\n"
                    "- Do not use any proper nouns (e.g., names of people, places, or specific organizations). Instead, use general terms"
                    "\nExample sentences:\n"
                    "- A man runs on the street.\n"
                    "- A dog jumps in the park.\n"
                    "- Please ensure you return 5 sentences describing a scene.\n"
                    "\nReturn all generated sentences as a single array of strings, where each sentence is an element of the array.\n"
                )

    # Prepare the prompt
    query_TTV = str(summerize_formal)

    # Define the messages
    messages_TTV = [
        {"role": "system", "content": system_role_TTI},
        {"role": "user", "content": query_TTV}
    ]

    # Make the request to the OpenAI API
    response_TTV = client.chat.completions.create(
        model=model,
        messages=messages_TTV,
    )

    # Print the response
    answer_TTV = response_TTV.choices[0].message.content
    print("Raw Response from TTV API:", answer_TTV)


    cleaned_response = re.sub(r'```python\n|\n```', '', answer_TTV)

    try:
        # JSON 형식으로 파싱 시도
        parsed_answer = json.loads(answer_TTV)
        
        if isinstance(parsed_answer, list):
            summerize_TTV = parsed_answer
        else:
            print("응답이 JSON 배열이 아닙니다. 기본 값을 설정합니다.")
            summerize_TTV = ["A scene description is unavailable."] * 5

    except json.JSONDecodeError:
        # JSON이 아닌 경우, 텍스트 배열로 전처리
        print("JSON 파싱 오류. 텍스트 배열로 처리 시도.")

        # 텍스트 배열 추출 (문자열 배열 형태로 가정)
        matches = re.findall(r'"(.*?)"', answer_TTV)
        
        if len(matches) == 5:
            summerize_TTV = matches
        else:
            print("텍스트 배열 형식도 예상과 다릅니다. 기본 값을 설정합니다.")
            summerize_TTV = ["A scene description is unavailable."] * 5
    
    sum=[summerize_casual, summerize_formal, summerize_TTV]

    return sum

if __name__=="__main__":
    sum=GPT(article)
