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

# Inject custom CSS for background color and image
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #f4f4f4, #d6e4f0), url("https://www.transparenttextures.com/patterns/diagmonds-light.png");
        background-size: cover;
        background-attachment: fixed;
        color: #333333;
    }
    h1 {
        font-family: 'Arial', sans-serif;
        color: #4CAF50;
        text-align: center;
    }
    p {
        font-family: 'Arial', sans-serif;
        color: #555555;
        font-size: 18px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app content
st.markdown('<h1>Jobify</h1>', unsafe_allow_html=True)
st.markdown('<p>Improve Your Resume ATS</p>', unsafe_allow_html=True)

jd = st.text_area("Paste the Job Description", help="Enter the job description here")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
