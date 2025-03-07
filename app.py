import streamlit as st
import os
from document_parser import parse_file
from ai import AI

st.set_page_config(
    page_title="Markdown Converter",
    layout="wide"
)

def main():
    st.title("Mardown Converter")
    st.markdown("Accept PDF, DOC and Jupyter Notebook -> proper latex and codeblock")

    upload = st.file_uploader("Open File", type=["pdf", "docx", "ipynb"])

    if "markdown_result" not in st.session_state:
        st.session_state.markdown_result = ""
    if "current_markdown" not in st.session_state:
        st.session_state.current_markdown= ""

    if upload is not None and st.button("Convert"):
        try:
            file_data = upload.getvalue()
            file_name = upload.name

            content, file_type = parse_file(file_data, file_name)
            
            st.info("File parsed successfully. Converting to Markdown")

            processor = AI()
            markdown_text = processor.convert_markdown(content, file_type)

            st.session_state.markdown_result = markdown_text
            st.session_state.current_markdown = markdown_text

        except Exception as e:
            st.error(f"error: {str(e)}")

    if st.session_state.markdown_result:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Markdown")

            edit_markdown = st.text_area(
                "Mardown Output",
                st.session_state.current_markdown,
                height=500,
            )

            st.session_state.current_markdown = edit_markdown

        with col2:
            st.subheader("Preview")
            st.markdown(st.session_state.current_markdown)

if __name__ == "__main__":
    main()