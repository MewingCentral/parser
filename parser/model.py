from enum import StrEnum
from pydantic import BaseModel
from typing import List, Union, Optional, Tuple

class PageType(StrEnum):
    SECTION = "Section"
    QUESTION = "Question"

class SectionType(StrEnum):
    BASIC_DATA_STRUCTURES = "Basic Data Structures"
    ADVANCED_DATA_STRUCTURES = "Advanced Data Structures"
    ALGORITHM_ANALYSIS = "Algorithm Analysis"
    ALGORITHMS = "Algorithms"

class TableCell(BaseModel, strict = True):
    content: Optional[str]
    # (x0, y0, x1, y0) coordinates of the cell
    rect: Optional[Tuple[float, float, float, float]] = None
    width: Optional[float] = None
    height: Optional[float] = None

class TableRow(BaseModel, strict = True):
    cells: List[TableCell]

class Table(BaseModel, strict = True):
    rows: List[TableRow]

class Graphics(BaseModel, strict = True):
    # table is currently the only implemented element.
    element_type: str
    # eventually, add Line, Circle, and anything else relevant.
    data: Union[Table]
    rect: Optional[Tuple[float, float, float, float]] = None
    width: Optional[float] = None
    height: Optional[float] = None
    
class Page(BaseModel, strict=True):
    page_type: PageType
    section_type: SectionType
    
    # 0-indexed page numbers, not including the section page
    page_number: int
    text: str

    graphics: List[Graphics] | None = None

class SubQuestion(BaseModel, strict=True):
    # text excluding the sub-question number and the "a) " prefix
    text: str
    
    # eg. "a", "b", "c"
    identifier: str
    sub_questions: List['SubQuestion']
    max_points: int | None = None

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

def table_as_string(table : Table) -> str:
    result = []
    for row in table.rows:
        row_str = " | ".join([cell.content for cell in row.cells])
        result.append(row_str)
    return "\n".join(result)

def tables_as_string(tables : List[Table]) -> str:
    tables_list = []
    for table_number, table in enumerate(tables):
        tables_list.append(f"Table {table_number + 1}:")
        for row in table.rows:
            row_str = " | ".join([cell.content if cell.content is not None else " " for cell in row.cells])
            tables_list.append(f"| {row_str} |")
        tables_list.append("")
        
    return "\n".join(tables_list)

def coordinates_as_string(graphics: List[Union[Graphics, Tuple[float, float, float, float]]]) -> str:
    result = []
    for graphic in graphics:
        if isinstance(graphic, tuple) and len(graphic) == 4:
            x0, y0, x1, y1 = graphic
            width = x1 - x0
            height = y1 - y0
            # pages are currently being treated as tables with widths of 612 and heights of 792
            # if this becomes an issue, I can fix it later but might not be necessary.
            result.append(f"Table Coordinates: {graphic}, Width: {width}, Height: {height}")
        
        elif isinstance(graphic, Graphics):
            if graphic.rect:
                rect = graphic.rect
                result.append(f"Graphics {graphic.element_type} - Rect: {rect}, Width: {graphic.width}, Height: {graphic.height}")

            if isinstance(graphic.data, Table):
                table = graphic.data
                for row_index, row in enumerate(table.rows):
                    for cell_index, cell in enumerate(row.cells):
                        if cell.rect:
                            result.append(f"Table Cell [Row {row_index}, Cell {cell_index}] - Rect: {cell.rect}, Width: {cell.width}, Height: {cell.height}")
        
        else:
            result.append(f"Unexpected graphic type: {type(graphic)}")

    return "\n".join(result)