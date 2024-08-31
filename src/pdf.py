from io import BytesIO
from pypdf import PdfReader


def read_pdf(file):
    """PDF 파일의 텍스트를 추출하여 반환합니다."""
    pdf_reader = PdfReader(BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:  # 페이지에서 텍스트를 성공적으로 추출했을 때만 추가
            text += page_text
    return text
