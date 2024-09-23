from parser.model import Section, Question, Page, SectionType, questions_as_string, PageType
from typing import List, Optional, Dict


import re

# Define the regex pattern to extract questions
question_pattern = re.compile(
    r"(?s)\s*([1-5])\)\s*\((\d+)\s*pts\)\s*(\w+)\s*\(\s*([^)]+?)\s*\)\s*(.*?)(?=\s*[1-5]\)\s*\(\d+\s*pts\)\s*\w+\s*\([^)]+\)|\s*\Z)",
    re.DOTALL
)


def get_questions(section: Section) -> List[Question]:
    questions: Dict[int, Question] = {}
    
    for i, page in enumerate(section.pages):
        assert page.page_type == PageType.QUESTION
        
        
        next: Optional[Page] = section.pages[i + 1] if i + \
            1 < len(section.pages) else None

        next_plus_current = apply_header_filter(page.text) + ("\n" + apply_header_filter(next.text) if next is not None else "")
        
        

        # Find all matches in the combined text of the current and next page

        current_questions: List[Question] = extract_questions(apply_header_filter(page.text), section.type)
        next_plus_current_questions: List[Question] = extract_questions(next_plus_current, section.type)
        
        
        for question in current_questions:
            question.pages.append(i + section.start_page)
            questions[question.question_number] = question
        
        
        for question in next_plus_current_questions:
            if question.question_number in questions:
                # this means that the question spanned multiple pages and the text spanning both pages should be updated
                
                if questions[question.question_number].text != question.text:
                    questions[question.question_number].text = question.text
                    assert next is not None
                    questions[question.question_number].pages.append(i + section.start_page + 1)

        write_to_file(f"current_questions_{i}.txt", "\n".join(questions_as_string(current_questions, include_metadata=True)))
        write_to_file(f"next_plus_current_questions_{i}.txt", "\n".join(questions_as_string(next_plus_current_questions, include_metadata=True)))
        
    return sorted(questions.values(), key=lambda q: q.question_number)
        
        
        
def write_to_file(filename: str, content: str):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Successfully wrote content to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to {
              filename}: {e}", file=sys.stderr)

        
        
def apply_header_filter(text: str) -> str:
    # remove the header and footer metadata
    
    
    new_text: List[str] = []
    text = text.split("\n")
    
    for line in text:
        if line.startswith("Page"):
            continue
        if line.startswith("Summer"):
            continue    
        if line.startswith("Spring"):
            continue    
        if line.startswith("Fall"):
            continue
        new_text.append(line)
    
    return "\n".join(new_text)
        



def extract_questions(text: str, section_type: SectionType) -> List[Question]:
    questions: List[Question] = []
    matches = question_pattern.findall(text)

    for match in matches:
        question_number, max_points, category, sub_category, text = match
        question = Question(
            pages=[],
            section_type=section_type,
            question_number=int(question_number),
            max_points=int(max_points),
            category=category,
            sub_category=sub_category,
            text=text.strip(),
            sub_questions=[]
            )
        questions.append(question)

    return questions
