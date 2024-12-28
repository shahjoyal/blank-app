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

# Inject custom CSS for teal theme with darker fonts
st.markdown(
    """
    <style>
    /* Background styling */
    .stApp {
        background: linear-gradient(to bottom, #dff7f6, #81d8d0);
        background-size: cover;
        background-attachment: fixed;
        color: #003333; /* Darker text color */
    }

    /* Title styling */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5em;
        color: #002626; /* Dark teal for better contrast */
        text-align: center;
        margin-bottom: 10px;
    }

    /* Subtitle styling */
    p {
        font-family: 'Roboto', sans-serif;
        font-size: 1.3em;
        color: #002626; /* Dark teal for better readability */
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Customize text inputs */
    textarea, .stFileUploader {
        font-family: 'Roboto', sans-serif;
        font-size: 1.1em;
        color: #002626; /* Dark teal font for inputs */
    }

    /* Button styling */
    button {
        background-color: #20b2aa !important;
        color: white !important;
        font-size: 1.2em !important;
        border-radius: 5px !important;
        padding: 8px 16px !important;
        font-family: 'Roboto', sans-serif !important;
    }

    /* Subheader styling */
    .stSubheader {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4em;
        color: #003333; /* Darker text for subheaders */
    }
    </style>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
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
