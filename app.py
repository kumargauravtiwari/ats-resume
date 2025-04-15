import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with Gemini API
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt Template with placeholders
def create_prompt(resume_text, jd_text):
    return f"""
    Hey Act Like a skilled or very experienced ATS (Applicant Tracking System) with a deep understanding of tech fields like software engineering, data science, data analysis, and big data engineering.

    Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and provide the best assistance for improving the resume.

    Assign the percentage match based on the JD and identify the missing keywords with high accuracy.

    resume: {resume_text}
    description: {jd_text}

    I want the response in one single string having the structure:
    {{
        "JD Match": "%",
        "MissingKeywords": [],
        "Profile Summary": ""
    }}
    """

# Streamlit UI
st.title("📄 Smart ATS Resume Evaluator")
st.text("Get your resume matched against a job description and optimize it!")

jd = st.text_area("📋 Paste the Job Description here")
uploaded_file = st.file_uploader("📁 Upload Your Resume (PDF)", type="pdf", help="Only PDF format is supported.")

submit = st.button("🚀 Submit")

if submit:
    if uploaded_file is not None and jd:
        with st.spinner("Analyzing Resume... Please wait."):
            resume_text = input_pdf_text(uploaded_file)
            prompt = create_prompt(resume_text, jd)
            response = get_gemini_response(prompt)

        st.subheader("📊 ATS Evaluation Result")
        try:
            parsed = json.loads(response)
            st.json(parsed)
        except Exception as e:
            st.write("⚠️ Couldn't parse response into JSON. Showing raw result:")
            st.text(response)
    else:
        st.warning("Please upload a resume and paste a job description.")
