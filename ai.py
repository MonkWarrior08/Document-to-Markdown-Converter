import os
from dotenv import load_dotenv
import openai

load_dotenv()

class AI():
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = api_key

    def convert_markdown(self, text, file_type):
        prompt = self.create_prompt(text, file_type)

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
                {"role": "system", "content": "You are a document converter specialized in reformatting text into clean, well-structured markdown. Pay special attention to mathematical formulas (convert to LaTeX) and code blocks (format properly with language hints)."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content

    def create_prompt(self, text, file_type):
        base_prompt = f"""
        Convert the following {file_type.upper()} document content into well-formatted markdown.

        Special instructions:
        1. Preserve the original structure as much as possible
        2. Format all mathematical formulas and equations using LaTeX:
           - Use single dollar signs ($) for inline math
           - Use double dollar signs ($$) for block equations, with the delimiters on separate lines like:
             $$
             math equation here
             $$
        3. Properly format code blocks with appropriate language hints
        4. Preserve tables, lists, and other structured elements
        5. Use appropriate markdown heading levels (# for main headings, ## for subheadings, etc.) but don't provide ```markdown
        6. For content that appears to be diagrams or complex visualizations, add a [DIAGRAM] placeholder and describe it briefly

        Here's the document content:

        {text}      
        """
        return base_prompt