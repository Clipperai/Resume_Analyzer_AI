import streamlit as st
from PyPDF2 import PdfReader 
from docx import Document # type: ignore
from groq import Groq 

client = Groq(api_key = st.secrets["GROQ_API_KEY"])

MODEL="openai/gpt-oss-safeguard-20b"

def ask_ai(prompt):
    response = client.chat.completions.create(
            model = MODEL,
            temperature = 0,
            messages = [{"role": "user", "content": prompt}]
        )
    return response.choices[0].message.content


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
role = st.selectbox('Job Description', ['-Select-', 'Python Dev', 'Frontend Dev', 'Backend Dev', 'Full Stack Dev', 'ML Dev', 'Data Analyst', 'AI Engineer'])
button = st.button("Submit")

if file and button:
    with st.spinner('Analyzing...'):
        resume_text = extract_text(file)

        if resume_text.strip() == "": # type: ignore
            st.error("Could not read file!")
        
        else:
             prompt = f"""
             STRICTLY FOLLOW THIS PROMPT
                Analyze this resume for a {role} role.
                
                Give:
                1. Summary (bullet points)
                2. Key Skills
                3. Strengths
                4. Missing Skills
                5. Improvements
                6. ATS score out of 100
                7. Required ATS score for this role
                
                Resume:
                {resume_text}
                """
            
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


