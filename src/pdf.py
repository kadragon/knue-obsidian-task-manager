from io import BytesIO
from pypdf import PdfReader


def read_pdf(file):
    """
    PDF 파일의 텍스트를 추출하여 반환합니다.
    """
    pdf_reader = PdfReader(BytesIO(file.read()))
    return ''.join(
        page.extract_text() or ''
        for page in pdf_reader.pages
    )
