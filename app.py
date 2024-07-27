import streamlit as st

import google.generativeai as genai
import os
import PyPDF2 as pdf
import fitz  # PyMuPDF
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text




## streamlit app

st.set_page_config(page_title="Resume Coach")
st.header("Resume Coach")
st.write("Upload your resume and enter your email for a review.")

email = st.text_input("Email")

input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Choose a file(PDF)",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None and email is not None and input_text is not None:
        pdf_content=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt1+"Resume"+pdf_content+"Job Description"+input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
       st.write("Please enter all details")

elif submit3:
    if uploaded_file is not None and email is not None and input_text is not None:
        pdf_content=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt3+"Resume"+pdf_content+"Job Description"+input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
       st.write("Please enter all details")

