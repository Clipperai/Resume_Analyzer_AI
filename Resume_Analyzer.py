import streamlit as st
from PyPDF2 import PdfReader 
from docx import Document # type: ignore
from brain import ask_ai


def extract_text(file):
    if file.type == 'application/pdf':
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text +=page.extract_text() or ""
            return text
    
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    
    else:
        return ""



if 'history' not in st.session_state:
    st.session_state.history = []


st.title("Resume Analyzer AI")

file = st.file_uploader("Upload a file", type=['pdf', 'docs'])
role = st.selectbox('Select', ['Frontend Dev', 'Backend Dev', 'Full Stack Dev', 'ML Dev', 'Data Analyst', 'AI Engineer'])

if file:
    with st.spinner('Analyzing...'):
        resume_text = extract_text(file)

        if resume_text.strip() == "": # type: ignore
            st.error("Could not read file!")
        
        else:
            result = ask_ai(resume_text)
            st.subheader("Analysis Result")
            st.write(result)
            st.session_state.history.append({
    "name": file.name,
    "content": result,
})



st.sidebar.header("Menu")

with st.sidebar.expander("View History"):
        for i in st.session_state.history:
            st.write(i)
        
        if st.button("Clear History"):
            st.session_state.history = []


