import sys
from pypdf import PdfReader
from pydantic import BaseModel
from typing import List, Tuple
from enum import StrEnum
import re

from parser.model import PageType, SectionType, Section, Page, pages_as_string, sections_as_string, questions_as_string, Question, tables_as_string, coordinates_as_string
from parser.page_processing import get_page_type, get_section_type
from parser.section_processing import get_sections
from parser.question_extraction import get_questions

from parser.vector_processing import extract_tables, extract_table_coordinates

class Question(BaseModel):
    id: int
    original_page_number: int
    filtered_page_number: int
    solutions_page_number: int
    text: str


class PreProcessedExam(BaseModel):
    sections: List[Section]

# from .types import Question
def main(input_file):
    try:
        # Open and read the PDF file
        reader = PdfReader(input_file)

        # Process the PDF content here
        # For example, you could extract text from each page:
        pages: List[Page] = []
        previous_section_type: SectionType | None = None
        for page_number, page in enumerate(reader.pages):
            if previous_section_type is None:
                assert page_number == 0
                
            text = page.extract_text()

            page_type = get_page_type(text)
            if page_type is None:
                print(f"Breaking on page {page_number} because it is not a valid PageType")
                break
            
            if page_type == PageType.SECTION:
                section_type = get_section_type(text)
                if section_type is None:
                    print(f"Breaking on page {
                        page_number} because it is not a valid SectionType")
                    print(text)
                    break
            else:
                section_type = previous_section_type
            
            page = Page(
                page_type=page_type,
                section_type=section_type,
                page_number=page_number,
                text=text
            )
            pages.append(page)
            
            previous_section_type = section_type

        print("Extracting tables from pdfs")
        tables = extract_tables(input_file)
        write_to_file("tables.txt", tables_as_string(tables))

        print("Extracting table coordinates from pdfs")
        table_dimensions = extract_table_coordinates(input_file)
        write_to_file("table_dimensions.txt", coordinates_as_string(table_dimensions))

        write_to_file("raw.txt", "\n".join(
            pages_as_string(pages, include_metadata=False)))
        write_to_file("raw_with_meta.txt", "\n".join(
            pages_as_string(pages, include_metadata=True)))

        sections: List[Section] = get_sections(pages)


        write_to_file("sections.txt", "\n".join(sections_as_string(sections, include_metadata=True)))

        for section in sections:
            questions = get_questions(section)
            section.questions = questions

        import json

        class Document(BaseModel):
            sections: List[Section]

        document = Document(sections=sections)

        # Write pydantic models to JSON file
        with open("document.json", "w") as json_file:
            json_file.write(document.model_dump_json())
        

        print("DONE")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def write_to_file(filename: str, content: str):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Successfully wrote content to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to {
              filename}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse.py <input_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
