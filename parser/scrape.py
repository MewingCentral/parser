# Testing beautiful soup for scraping PDFs from FE website

import requests 
from bs4 import BeautifulSoup
import re
import os

url = "https://www.cs.ucf.edu/registration/exm/"
read = requests.get(url) # Get request for HTML
html = read.content
soup = BeautifulSoup(html, "html.parser")

# Is the tag a PDF link for an exam that has no discrete section?
def pdf_before_discrete(tag):
    return tag.name == "a" and re.search(".pdf", tag["href"]) and not re.search("CS|DS", tag["href"])

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

    for doc in chunk:
        cur_link = doc.get("href")
        response = requests.get(url + cur_link)
        file_name = cur_link.rsplit('/', 1)[-1]
        pdf = open(pdfs_dir + "/" + dir_name + "/" + file_name, 'wb')
        pdf.write(response.content)
        pdf.close()
        