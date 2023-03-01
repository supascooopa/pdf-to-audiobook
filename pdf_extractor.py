from PyPDF2 import PdfReader


def read_pdf(pdf_path):
    pdf_reader = PdfReader(pdf_path).pages[0]
    return pdf_reader.extract_text()

