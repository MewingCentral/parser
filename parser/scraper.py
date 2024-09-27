# Testing beautiful soup for scraping PDFs from FE website

import requests 
from bs4 import BeautifulSoup
import re
import os

url = "https://www.cs.ucf.edu/registration/exm/"
read = requests.get(url) # Get request for HTML
html = read.content
soup = BeautifulSoup(html, "html.parser")

pdf_anchors = soup.find_all(href=re.compile("pdf"))
pdf_anchors[0]
# print(bool(re.search(r"sol", "FE_sol.pdf", re.IGNORECASE)))

# Make directories to store PDFs
exams_dir = "exams"
sols_dir = "exam_sols"
if (not os.path.exists(exams_dir)):
    os.makedirs(exams_dir)
if (not os.path.exists(sols_dir)):
    os.makedirs(sols_dir)

for pdf_anchor in pdf_anchors:
    cur_link = pdf_anchor.get('href')
    # Only save pdfs for exams and solution documents
    if ('.pdf' in cur_link and not('Info' in cur_link)):
        response = requests.get(url + cur_link)

        path = "exam_sols/" if "Sol" in cur_link else "exams/"
        path += cur_link.rsplit('/', 1)[-1]
        # print(path)

        pdf = open(path, 'wb')
        pdf.write(response.content)
        pdf.close()
