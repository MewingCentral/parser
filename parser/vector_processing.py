from parser.model import Section, SectionType, Page, Table, TableCell, TableRow
from typing import List

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