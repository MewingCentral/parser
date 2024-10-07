from parser.model import Section, SectionType, Page, Table, TableCell, TableRow
from typing import List, Tuple

import pdfplumber
    
def extract_tables(input_file : str) -> List[Table]:
    """Enumerates all pages of a provided FE and extracts the largest table on each page.
    
    """
    tables: List[Table] = []

    with pdfplumber.open(input_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            raw_table = page.extract_table()

            if raw_table is None:
                print(f"No table found on page {page_number}")
                continue
            print(f"Table found on page {page_number}")

            table_coordinates = page.bbox
            print(f"Bounding box data for the page:")
            print(f"Page number {page_number} and coordinates {table_coordinates}")
            
            table_rows = []
            for raw_row in raw_table:
                print(f"At least 1 table found page {page_number}.")
                if raw_row is None:
                    continue
                row_cells = [TableCell(content=cell if cell is not None else "") for cell in raw_row]
                table_rows.append(TableRow(cells=row_cells))

            if table_rows:
                tables.append(Table(rows=table_rows))

    return tables

def extract_table_coordinates(input_file : str) -> List[Tuple[float, float, float, float]]:
    """
    Extracts the x0, y0, x1, and y1 of all rectangular vector graphics on each page of the provided FE. currently,
    pages are being considered vector graphics as well by this processing algorithm. 

    Parameter:
    - input_file (str) : path to the FE exam file.

    Returns:
    - table_dimensions (list of tuples) : list of tuples containing 4 coordinates for each table located on every page.
        - x0 (float) : Distance of left side of rectangle from left side of page.
        - y0 (float) : Distance of bottom of rectangle from bottom of page.
        - x1 (float) : Distance of right side of rectangle from left side of page.
        - y1 (float) : Distance of top of rectangle from bottom of page.
    """

    rectangles = []

    with pdfplumber.open(input_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            page = pdf.pages[page_number]
            
            for rect in page.objects.get('rect', []):
                rectangles.append((rect['x0'], rect['y0'], rect['x1'], rect['y1']))

    return rectangles