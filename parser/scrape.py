# Testing beautiful soup for scraping PDFs from FE website

import requests 
from bs4 import BeautifulSoup
import re
import os
import json

json_output = {"documents":{}}

url = "https://www.cs.ucf.edu/registration/exm/"
read = requests.get(url) # Get request for HTML
html = read.content
soup = BeautifulSoup(html, "html.parser")

# Is the tag a PDF link for an exam that has no discrete section?
def pdf_before_discrete(tag):
    return tag.name == "a" and re.search(".pdf", tag["href"]) and not re.search("CS|DS", tag["href"])

# Return a string containing the semester and year of the exam specified
def get_semester_and_year(file_name):
    retval = ""

    # Get semester
    if (re.search(r"(jan)|(feb)|(mar)|(apr)", file_name, re.IGNORECASE) != None):
        retval = "spring"
    elif (re.search(r"(may)|(jun)|(jul)", file_name, re.IGNORECASE)):
        retval = "summer"
    else: 
        retval = "fall"

    # Get year
    retval += re.findall(r"[0-9]+", file_name)[0]
    return retval

# Return a string describing the type of exam document
def get_document_type(file_name):
    if (re.search(r"sol", file_name, re.IGNORECASE)):
        return "solutions"
    elif (re.search(r"info", file_name, re.IGNORECASE)):
        return "info"
    else:
        return "exam"

pdf_anchors = soup.find_all(pdf_before_discrete)

pdfs_dir = "pdfs"
if (not os.path.exists(pdfs_dir)):
    os.makedirs(pdfs_dir)

for i in range(0, len(pdf_anchors), 3):
    # A chunk corresponds to all docs for a single exam
    chunk = pdf_anchors[i:i+3]

    # Make the directory for the current exam
    dir_name = re.findall(r"/(.*)\.", chunk[0].get("href"))[0]
    if (not os.path.exists(pdfs_dir + "/" + dir_name)):
        os.makedirs(pdfs_dir + "/" + dir_name)

    # Configure json output
    exam = get_semester_and_year(dir_name) + "_paths"
    json_output["documents"][exam] = {}

    for doc in chunk:
        cur_link = doc.get("href")
        response = requests.get(url + cur_link)

        file_name = cur_link.rsplit('/', 1)[-1]
        doc_type = get_document_type(file_name)
        path = pdfs_dir + "/" + dir_name + "/" + file_name

        # Configure json output
        json_output["documents"][exam][doc_type] = path

        pdf = open(path, 'wb')
        pdf.write(response.content)
        pdf.close()

output_file = open("exam_paths.json", "w")
output_file.write(json.dumps(json_output))
output_file.close()

        