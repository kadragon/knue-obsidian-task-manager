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


def save_pdf_file(final_dir, file):
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    try:
        with open(os.path.join(final_dir, file.name), 'wb') as f:
            f.write(file.getbuffer())

        return True
    except:
        return False
