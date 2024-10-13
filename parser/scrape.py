# Scrapes and stores all PDFs from the previous FE webpage

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
def pdf_after_discrete(tag):
    is_anchor = tag.has_attr("href")
    contains_pdf = is_anchor and re.search(".pdf", tag["href"])
    pdf_not_labeled_with_CS_or_DS = contains_pdf and not re.search("CS|DS", tag["href"])

    if (pdf_not_labeled_with_CS_or_DS):
        # All exams after August 2016 contain no discrete section
        exam_date = tag.parent.parent.contents[0].get_text()
        year_match = re.search(r"[0-9]+$", exam_date)
        if year_match:
            year = int(year_match.group())
            # Return true if the exam was after August 2016
            return (year > 2016) or (year == 2016 and not re.search("aug|may", exam_date, re.IGNORECASE))

    return False

# Return a string describing the type of exam document
def get_document_type(file_name):
    if (re.search(r"sol", file_name, re.IGNORECASE)):
        return "solutions"
    elif (re.search(r"info", file_name, re.IGNORECASE)):
        return "info"
    else:
        return "exam"

pdf_anchors = soup.find_all(pdf_after_discrete)

pdfs_dir = "pdfs"
if (not os.path.exists(pdfs_dir)):
    os.makedirs(pdfs_dir)

for i in range(0, len(pdf_anchors), 3):
    # A chunk corresponds to all docs for a single exam
    chunk = pdf_anchors[i:i+3]

    # Make the directory for the current exam
    dir_name = re.findall(r"^[^\/]+", chunk[0].get("href"))[0]
    if (not os.path.exists(pdfs_dir + "/" + dir_name)):
        os.makedirs(pdfs_dir + "/" + dir_name)

    # Configure json output
    json_output["documents"][dir_name] = {}

    for doc in chunk:
        cur_link = doc.get("href")
        response = requests.get(url + cur_link)

        file_name = cur_link.rsplit('/', 1)[-1]
        doc_type = get_document_type(file_name)
        path = pdfs_dir + "/" + dir_name + "/" + file_name

        # Configure json output
        json_output["documents"][dir_name][doc_type] = path

        pdf = open(path, 'wb')
        pdf.write(response.content)
        pdf.close()

output_file = open("exam_paths.json", "w")
output_file.write(json.dumps(json_output))
output_file.close()

        