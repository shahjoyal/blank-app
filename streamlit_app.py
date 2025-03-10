import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re  # Import regex to clean AI output

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Gemini 2 model
    response = model.generate_content(input, stream=False)  # Ensures full response
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text() or ""  # Handle NoneType
    return text.strip()  # Remove unwanted spaces

# Streamlit UI Styling
st.set_page_config(page_title="Jobfy - ATS Matcher", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #E3F2FD; /* Light bluish background */
        }
        .stApp {
            background-color: #E3F2FD;
        }
    </style>
""", unsafe_allow_html=True)

# UI Title
st.title("Jobfy - Resume ATS Matcher")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description")

# Submit button should always be available
submit_button = st.button("Submit")

if submit_button and uploaded_file and job_description:
    st.write("Processing...")
    
    # Extract text from PDF
    resume_text = input_pdf_text(uploaded_file)
    
    # Create input prompt
    input_prompt = f"""
    Act as an ATS (Applicant Tracking System) with expertise in software engineering, data science, and big data engineering.

    Your task:
    1. Analyze the resume and compare it with the job description.
    2. Assign a **matching percentage** based on JD.
    3. List **missing keywords** required for the role.
    4. Generate a **profile summary**.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return the response **strictly in JSON format** (DO NOT include explanations, Markdown, or extra text):

    {{
      "JD Match": "XX%",
      "MissingKeywords": ["keyword1", "keyword2"],
      "Profile Summary": "Your profile summary goes here."
    }}
    """
    
    # Get AI response
    response_text = get_gemini_response(input_prompt)
    
    # Ensure AI output is valid JSON
    try:
        cleaned_response = re.sub(r"```json|```", "", response_text).strip()  # Remove markdown formatting
        response_json = json.loads(cleaned_response)  # Convert cleaned string to JSON
        
        # Display response in cards
        st.markdown("### Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='padding: 15px; background-color: white; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);'>
                    <h4 style='color: #007BFF;'>ATS Match Score</h4>
                    <p style='font-size: 20px; font-weight: bold;'>{}</p>
                </div>
            """.format(response_json["JD Match"]), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='padding: 15px; background-color: white; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);'>
                    <h4 style='color: #FF5722;'>Missing Keywords</h4>
                    <p>{}</p>
                </div>
            """.format(", ".join(response_json["MissingKeywords"])), unsafe_allow_html=True)
        
        st.markdown("""
            <div style='padding: 15px; background-color: white; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-top: 20px;'>
                <h4 style='color: #4CAF50;'>Profile Summary</h4>
                <p>{}</p>
            </div>
        """.format(response_json["Profile Summary"]), unsafe_allow_html=True)
    
    except json.JSONDecodeError:
        st.error("AI response is not in valid JSON format. Please try again.")
        st.text_area("Raw AI Response", response_text)  # Show raw output for debugging
