# Document to Markdown Converter
<img width="1750" alt="Screenshot 2025-03-08 at 2 03 54 PM" src="https://github.com/user-attachments/assets/cb292a1b-23f5-410e-bb82-5b86c1117a03" />

A simple interface built with Streamlit that allows you to upload documents (PDF, DOCX, IPYNB) and convert them to well-formatted Markdown with the aid of OpenAI. The application uses OpenAI to process and improve the formatting, with special attention to:

- Mathematical formulas (converted to LaTeX)
- Code blocks (properly formatted)
- Overall text structure and readability

## Features

- Upload various document types (PDF, DOCX, Jupyter Notebooks)
- Extract and preserve document structure
- Format mathematical formulas using LaTeX syntax
- Properly format code blocks
- Generate clean Markdown output ready for use with AI systems

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the application with:

```
streamlit run app.py
```

Then upload a document through the web interface and click "Convert to Markdown". The converted markdown will be displayed and available for copying. 
