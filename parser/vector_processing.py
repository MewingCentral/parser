from parser.model import Section, SectionType, Page, Table, TableCell, TableRow
from typing import List

import pdfplumber
    
# function to extract the largest table on a provided page
def extract_tables(input_file : str) -> List[Table]:
    """Enumerates all pages of a provided FE and extracts the largest table on each page.
    
    """
    tables: List[Table] = []

    with pdfplumber.open(input_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # customize 'extract_table' settings to account for empty cells.
            
            raw_table = page.extract_table({
                "snap_tolerance": 3
            })

            if raw_table is None:
                print(f"No table found on page {page_number}")
                continue

            table_rows = []
            for raw_row in raw_table:
                print(f"Largest table found on {page_number}.")
                if raw_row is None:
                    continue
                row_cells = [TableCell(content=cell if cell is not None else "") for cell in raw_row]
                table_rows.append(TableRow(cells=row_cells))

            if table_rows:
                tables.append(Table(rows=table_rows))

    return tables