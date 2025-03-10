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
    model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Gemini 2 model
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Updated Prompt Template to enforce JSON format
input_prompt = """
Hey, act like an ATS (Applicant Tracking System) with expertise in software engineering, data science, and big data engineering.

Your task:
1. Analyze the resume and compare it with the job description.
2. Assign a **matching percentage** based on JD.
3. List **missing keywords** required for the role.
4. Generate a **profile summary**.

⚠️ **Return the response strictly in JSON format:**
```json
{{
  "JD Match": "XX%",
  "MissingKeywords": ["keyword1", "keyword2"],
  "Profile Summary": "Your profile summary goes here."
}}
```
"""
