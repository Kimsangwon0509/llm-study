import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

import retriever

import os
import dotenv as dotenv

dotenv.load_dotenv()
api_key = os.getenv("DEV_OPENAI_API_KEY")

# 모델 초기화
llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=api_key)

# 사용자의 메세지를 처리하는 함수
def get_ai_response(messages, docss):
    response1 = retriever.document_chain.stream(
        {
            "messages":messages,
            "contexts":docss,
        }
    )
    for chunk in response1:
        yield chunk

# streamlit 앱
st.title("GPT-4o LANGCHAIN APP")

# 스트림릿 session state 에 메세지 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage("너는 문서에 기반해 답변하는 도시 정책 전문가야.")
    ]

# 스트림릿 화면에 메세지 출력
for msg in st.session_state.messages:
    if msg.content:
        if isinstance(msg, SystemMessage):
            st.chat_message("system").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)

# 사용자 입력 처리
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(prompt))
    print("user\t: ",prompt)

    augmented_query = retriever.query_augmentation_chain.invoke({
        "messages" : st.session_state.messages,
        "query":prompt
    })
    print("augmented_query: ",augmented_query)
    '''
    with st.spinner(f"AI가 답변을 준비중입니다....{augmented_query}") :
        response = get_ai_response(st.session_state.messages)
        result = st.chat_message("assistant").write_stream(response)
    st.session_state.messages.append(AIMessage(result))
    '''
    print("관련 문서 검색")
    docs = retriever.retriever.invoke(f"{prompt}\n{augmented_query}")
    for doc in docs:
        print(doc)

        with st.expander(f"**문서:** {doc.metadata.get('source','알 수 없음')}"):
            # 파일명과 페이지 정보 표시
            st.write(f"**page** {doc.metadata.get('page','')}")
            st.write(doc.page_content)
    print('===========================')

    with st.spinner(f"AI가 답변을 준비 중입니다....{augmented_query}") :
        response = get_ai_response(st.session_state.messages, docs)
        result = st.chat_message("assistant").write_stream(response)
    st.session_state.messages.append(AIMessage(result))


