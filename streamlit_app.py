import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    /* App background and font styles */
    .stApp {
        background: linear-gradient(to bottom, #e0f7fa, #b2ebf2);
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Roboto', sans-serif;
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5em;
        color: #004d40;
        text-align: center;
    }

    p {
        text-align: center;
        font-size: 1.2em;
        color: #004d40;
    }

    /* Styling for response boxes */
    .ats-score-box, .suggestions-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    .ats-score-box h3, .suggestions-box h3 {
        color: #004d40;
        font-size: 1.5em;
    }

    .ats-score-box {
        border-left: 5px solid #26a69a;
    }

    .suggestions-box {
        border-left: 5px solid #00796b;
    }

    .suggestions-box p {
        color: #004d40;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app content
st.markdown('<h1>Jobify</h1>', unsafe_allow_html=True)
st.markdown('<p>Evaluate Your Resume with ATS</p>', unsafe_allow_html=True)

jd = st.text_area("Paste the Job Description", help="Enter the job description here")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        response_data = json.loads(response)

        # Display ATS Score in a separate box
        st.markdown(
            f"""
            <div class="ats-score-box">
                <h3>ATS Match Score: {response_data['JD Match']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display suggestions in another box
        st.markdown(
            f"""
            <div class="suggestions-box">
                <h3>Suggestions</h3>
                <p><strong>Missing Keywords:</strong> {', '.join(response_data['MissingKeywords'])}</p>
                <p><strong>Profile Summary:</strong> {response_data['Profile Summary']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
