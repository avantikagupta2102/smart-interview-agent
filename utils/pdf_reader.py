from pypdf import PdfReader

def read_pdf(file_object):
    # This reads the PDF directly out of Streamlit's RAM buffer
    reader = PdfReader(file_object)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text
