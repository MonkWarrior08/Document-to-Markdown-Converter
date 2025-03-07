import os
import io
from typing import Tuple
import PyPDF2
import docx
import docx.table
import docx.text
import docx.text.paragraph
import nbformat

def parse_file(file_data: bytes, file_name:str) -> Tuple[str,str]:
    extension = os.path.splitext(file_name)[1].lower()

    if extension == ".pdf":
        return parse_pdf(file_data), 'pdf'
    elif extension == ".docx":
        return parse_docx(file_data), 'docx'
    elif extension == ".ipynb":
        return parse_ipynb(file_data), 'ipynb'
    else:
        raise ValueError(f"unsupported: {extension}")
    
def parse_pdf(file_data: bytes) -> str:
    text = ""
    pdf_file = io.BytesIO(file_data)
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        if page_num < len(pdf_reader.pages) - 1:
            text += "\n\n---Page Break---\n\n"
    return text
    
def parse_docx(file_data: bytes) -> str:
    text = ""
    docx_file = io.BytesIO(file_data)
    doc = docx.Document(docx_file)

    for item in doc._body._body:
        if item.tag.endswith('p'):
            p = docx.text.paragraph.Paragraph(item, doc)
            if p:
                text += p.text + "\n"
        elif item.tag.endswith('tbl'):
            text += "\n"
            tbl = docx.table.Table(item, doc)
            for row in tbl.rows:
                row_text = [cell.text for cell in row.cells]
                text += "|".join(row_text) + "\n"
            text += "\n"
    return text

def parse_ipynb(file_data: bytes) -> str:
    text = ""
    file_content = file_data.decode("utf-8")
    notebook = nbformat.reads(file_content, as_version=4)

    for cell_num, cell in enumerate(notebook.cells):
        if cell.cell_type == 'markdown':
            text += f"### Markdown Cell {cell_num + 1}\n\n"
            text += cell.source + "\n\n"
        elif cell.cell_type == 'code':
            text += f"### Code Cell {cell_num + 1}\n\n"
            text += "```python\n"
            text += cell.source + "\n"
            text += "```\n\n"

            if hasattr(cell, "outputs") and cell.outputs:
                text += "Output:\n\n"
                for output in cell.outputs:
                    if 'text' in output:
                        text += "```\n" + "".join(output.text) + "\n```\n\n"
                    elif 'data' in output:
                        if 'text/plain' in output.data:
                            text += "```\n" + output.data['text/plain'] + "\n```\n\n"
    return text