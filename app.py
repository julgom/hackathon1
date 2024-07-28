import streamlit as st
from bs4 import BeautifulSoup
import shutil
import pathlib
import logging

import google.generativeai as genai
import os
import PyPDF2 as pdf
import fitz  # PyMuPDF
import json
from dotenv import load_dotenv

def add_analytics_tag():
    # replace G-XXXXXXXXXX to your web app's ID
    
    analytics_js = """
   
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XSZKX1MP02"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-XSZKX1MP02');
    </script>
    
    """
    analytics_id = "G-XSZKX1MP02"
    
    # Identify html path of streamlit
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=analytics_id): # if id not found within html file
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # backup recovery
        else:
            shutil.copy(index_path, bck_index)  # save backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + analytics_js) 
        index_path.write_text(new_html) # insert analytics tag at top of head
        
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
uploaded_file=st.file_uploader("Choose a file(PDF)",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit = st.button("Submit")

input_prompt = """You are an AI Resume Coach, an expert in helping individuals 
create compelling and professional resumes. Your primary role is to guide users in enhancing 
their resumes to improve their chances of securing job interviews. Here are your key tasks:
Resume Review: Carefully analyze the user's existing resume, providing constructive feedback on formatting, 
content, and overall presentation. Content Enhancement: Offer specific suggestions to improve the language, 
tone, and clarity of each section. Focus on making job responsibilities and achievements more impactful using 
action verbs and quantifiable results. Industry-Specific Advice: Tailor your recommendations based on the user’s 
target industry and role, ensuring that the resume meets industry standards and highlights relevant skills and 
experiences. Keyword Optimization: Help the user optimize their resume with appropriate keywords to pass through 
Applicant Tracking Systems (ATS). Section Organization: Guide the user on the most effective way to organize their 
resume sections, such as Professional Summary, Skills, Work Experience, Education, and Additional Information. 
Question Answering: Respond to specific queries from users regarding resume writing best practices, such as how to 
handle employment gaps, career changes, or lack of experience. Here is a resume to reveiw below:
"""

if submit:
    if uploaded_file and email:
        pdf_content=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt + " " + pdf_content)
        st.subheader("The Response is")
        st.write(response)
    elif uploaded_file and not email:
       st.write("Please enter the email")
    elif not uploaded_file and email:
       st.write("Please upload the resume")
    else:
       st.write("Please enter all details")

