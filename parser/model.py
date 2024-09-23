from enum import StrEnum
from pydantic import BaseModel
from typing import List

class PageType(StrEnum):
    SECTION = "Section"
    QUESTION = "Question"

class SectionType(StrEnum):
    BASIC_DATA_STRUCTURES = "Basic Data Structures"
    ADVANCED_DATA_STRUCTURES = "Advanced Data Structures"
    ALGORITHM_ANALYSIS = "Algorithm Analysis"
    ALGORITHMS = "Algorithms"
    
class Page(BaseModel, strict=True):
    page_type: PageType
    section_type: SectionType
    
    # 0-indexed page numbers, not including the section page
    page_number: int

    text: str



class SubQuestion(BaseModel, strict=True):
    # text excluding the sub-question number and the "a) " prefix
    text: str
    
    # eg. "a", "b", "c"
    identifier: str
    max_points: int

class Question(BaseModel, strict=True):
    pages: List[int]
    section_type: SectionType
    question_number: int
    max_points: int
    category: str
    sub_category: str
    # text excluding the question number, category, max points, and sub-questions
    text: str
    
    sub_questions: List[SubQuestion]

class Section(BaseModel, strict=True):
    # 0-indexed page numbers, not including the section page
    start_page: int
    end_page: int

    type: SectionType
    pages: List[Page]
    questions: List[Question] | None = None



def pages_as_string(pages: List[Page], include_metadata: bool = False) -> List[str]:
    result = []
    for page in pages:
        if include_metadata:
            result.append(f"Page {page.page_number}, SectionType: {page.section_type}, PageType: {page.page_type}")
        result.append(page.text)
    return result

def sections_as_string(sections: List[Section], include_metadata: bool = False) -> List[str]:
    result = []
    for section in sections:
        if include_metadata:
            result.append(f"Section {section.type}, StartPage: {section.start_page}, EndPage: {section.end_page}")
        result.append("\n".join(pages_as_string(section.pages, include_metadata=include_metadata)))
    return result


def questions_as_string(questions: List[Question], include_metadata: bool = False) -> List[str]:
    result = []
    for question in questions:
        if include_metadata:
            result.append(f"Question {question.question_number}, SectionType: {question.section_type}, Category: {question.category}, SubCategory: {question.sub_category}")
        result.append(question.text)
    return result