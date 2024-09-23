import sys
from pypdf import PdfReader
from pydantic import BaseModel
from typing import List, Tuple
from enum import StrEnum
import re

from parser.model import PageType, SectionType, Section, Page, pages_as_string, sections_as_string, questions_as_string, Question
from parser.page_processing import get_page_type, get_section_type
from parser.section_processing import get_sections
from parser.question_extraction import get_questions
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
                print(f"Breaking on page {
                      page_number} because it is not a valid PageType")
                break
            
            if page_type == PageType.SECTION:
                section_type = get_section_type(page_type, text)
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

        write_to_file("raw.txt", "\n".join(
            pages_as_string(pages, include_metadata=False)))
        write_to_file("raw_with_meta.txt", "\n".join(
            pages_as_string(pages, include_metadata=True)))

        sections: List[Section] = get_sections(pages)


        write_to_file("sections.txt", "\n".join(sections_as_string(sections, include_metadata=True)))


        basic_data_structures_section = next(
            (section for section in sections if section.type == SectionType.BASIC_DATA_STRUCTURES), None
        )

        write_to_file("basic_data_structures_sections.txt", "\n".join(
            sections_as_string([basic_data_structures_section], include_metadata=True)))
        
        questions = get_questions(basic_data_structures_section)

        write_to_file(f"questions_basic_data_structures.txt", "\n".join(questions_as_string(questions, include_metadata=True)))

        

        #for i, section in enumerate(sections):
        #    questions = get_questions(section)

        #    write_to_file(f"questions_{i}.txt", "\n".join(questions_as_string(questions, include_metadata=True)))
        #    continue


        # text_pages = filter_section_pages(text_pages)
        # write_to_file("filtered_out_section_pages.txt", "\n".join(text_pages))

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
