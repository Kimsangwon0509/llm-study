import sys

import pymupdf
import os
from dotenv import load_dotenv
from openai import OpenAI

from chap02 import client, response

load_dotenv()
api_key = os.getenv('API_KEY')

def summarize_txt(file_path : str):
    client = OpenAI(api_key=api_key)

    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    system_prompt = \
    f'''
    너는 다음 글을 요약하는 봇이다. 다음 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.
    
    ============ 이하 텍스트 ===============
    {txt}
    '''
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {"role" : "system", "content" : "system_promt"}
        ]
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    file_path = '../chap04/data/소프트웨어사업영향평가_가이드라인_1810152_with_preprocessing.txt'
    result_file_path = '../chap04/data/소프트웨어사업영향평가_가이드라인_1810152_with_preprocessing_result.txt'
    summary = summarize_txt(file_path)
    print(summary)

    with open(result_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)

