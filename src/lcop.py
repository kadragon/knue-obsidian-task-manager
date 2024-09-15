from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.vectorPinecone import VectorDatabasePinecone


todayDT = datetime.today().strftime("%Y-%m-%d")
vdp = VectorDatabasePinecone()


def get_analytic_result(text, openai_api_key, classification, tag, is_official_document=True):
    result = vdp.query(namespace="test", query=text)
    reference = ''.join([r.metadata['content'] for r in result.matches])

    llm = ChatOpenAI(model_name="gpt-4o-mini",
                     temperature=0.2, openai_api_key=openai_api_key)

    template = """
전문 {document_type} 분석 AI 어시스턴트로서, 제시된 {content_type}을 분석하고 업무 노트를 생성하는 작업을 수행합니다. 아래의 지침을 따라 간결하고 구조화된 요약을 제공해 주세요.

😀 Emojis: On

1. Provide a summary in the following format:

# {title_type} (원문의 {content_type} {title_type}을 {title_action})

## 🙋‍♂️ 관련
(아래 내용 반드시 추가)
- {{classification}}
- {{tag}}

{related_documents_section}

## 📢 현황 및 문제점
- {content_type}을 읽는 사람 입장에서 핵심 내용을 3~5줄(- 으로 구분) 이내로 요약
- 주요 결정사항, 정책 변경, 또는 요구사항을 중심으로 작성
- 마침표는 표기하지 말고, 기간이나 날짜를 표기할 경우, YYYY.m.d 형식을 사용

## 🛠 해결 방안
- 문서에서 명시적으로 언급된 후속 조치나 할일 사항을 나열
- 후속 조치 사항이 없는 경우 해결 방안 절을 생략
- {deadline_instruction}
- 필요하다면 이전 업무 노트도 참고해서 해결 방안을 작성
- 예시:
  - [ ] 할일 1 📅 YYYY-MM-DD
  - [ ] 할일 2 📅 YYYY-MM-DD

{additional_instructions}

3. Carefully analyze the following text:
{{texts}}

4. 이전 업무 노트
{{reference}}
"""

    if is_official_document:
        document_type = "공문"
        content_type = "공문"
        title_type = "공문 제목"
        title_action = "정확히 기재"
        related_documents_section = """
## 관련 공문
- 관련 문서가 있는 경우에만 작성하며, 없으면 이 절을 생략
- 발신처, 문서번호, 날짜 사이에 띄어쓰기를 하지 않음, 공문제목이 없을경우 공문제목은 표기하지 않음
- 형식: [[문서번호(YYYY.m.d)]] 공문제목 or 「규정명」 제조(항목)
- 예시:
  - 1. [[교육정보원-1234(2024.1.2)]] 공문제목
  - 2. [[총무과-4567(2024.3.7)]] 공문제목
  - 3. 「한국교원대학교 교육정보원 규정」 제5조(직무)
"""
        deadline_instruction = "명확한 날짜 제한이 없다면 {todayDT}로 설정"
        additional_instructions = """
2. "## 관련 공문"에 아래 내용 추가
- 제시된 공문의 하단에 있는 공문 번호
- 형식: [[부서명-문서번호(YYYY.m.d)]]
- 발신처, 문서번호, 날짜 사이에 띄어쓰기를 하지 않음

이 지침을 바탕으로 공문을 분석하고 업무 노트를 작성해 주세요.
"""
    else:
        document_type = "요청"
        content_type = "내용"
        title_type = "할일 제목"
        title_action = "분석해서 주요 제목 추출"
        related_documents_section = ""
        deadline_instruction = "기본적으로 일자 처리가 없을 경우, 오늘 날짜({todayDT})를 마감일로 입력"
        additional_instructions = "이 지침을 바탕으로 공문을 분석하고 업무 노트를 작성해 주세요."

    prompt = PromptTemplate.from_template(template.format(
        document_type=document_type,
        content_type=content_type,
        title_type=title_type,
        title_action=title_action,
        related_documents_section=related_documents_section,
        deadline_instruction=deadline_instruction,
        additional_instructions=additional_instructions
    ))

    chain = prompt | llm

    response = chain.invoke(
        {"texts": text, "classification": classification, "tag": tag, "todayDT": todayDT, "reference": reference})

    return response.content
