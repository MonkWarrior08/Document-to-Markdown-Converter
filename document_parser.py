import os
import io
from typing import Tuple
import PyPDF2
import docx
import nbformat

def parse_file(file_data: bytes, file_name:str) -> Tuple[str,str]:
    extension = os.path.splitext(file_name)[1].lower()

    if extension == ".pdf":
        return parse_pdf(file_data), 'pdf'
    elif extension == ".docx":
        return parse_docx(file_data), '.docx'
    elif extension == ".ipynb":
        return parse_ipynb(file_data), '.ipynb'
    else:
        raise ValueError(f"unsupported: {extension}")
    
def parse_pdf(file_data: bytes) -> str:
    text = ""
    pdf_file = io.BytesIO(file_data)
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        if page_num < len(pdf_reader.pages) - 1:
            text += "\n\n---Page Break---\n\n"
        return text
    
def parse_docx(file_data: bytes) -> str:
    text = ""
    docx_file = io.BytesIO(file_data)
    docx_reader = docx.Document(docx_file)

    for para in docx_reader.paragraphs:
        text += para.text + "\n"

    for table in docx_reader.tables:
        text += "\n"
        for row in table.rows:
            row_text = [cell.text for cell in row.cells]
            text += "|".join(row_text) + "\n"
        text += "\n"
    return text