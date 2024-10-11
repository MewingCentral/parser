from typing import List, Tuple
import re
from parser.model import PageType, SectionType, Page




def extract_section_info(text: str) -> Tuple[str, str]:
    """
    Extracts section letter and name from a string containing "Section A: XYZ" format.
    
    Args:
    text (str): The input string containing section information.
    
    Returns:
    Tuple[str, str]: A tuple containing the section letter and section name.
    """

    # Looking for the following 2 lines:
    # Section A 
    # BASIC DATA STRUCTURES
    # post 2022 exam regex
    match = re.search(r"Section\s+([A-D])(?:\s+|\n)(.*?)(?:\n|$)", text, re.DOTALL)
    #print("0", match)
    if match is None:
        #print("unable to get section letter using Regex, must be pre 2022 Exam")
        # Looking for the following 2 lines:
        # Section I  A  
        # DATA STRUCTURES  
        # pre 2022 exam regex
        match = re.search(r"Section\s+([I|I I]+)\s+([A-Z])\s*\n(.*?)(?:\n|$)", text, re.DOTALL)
        #print("1", match)
        #print("initial match: ", match)
        if match:
            #print("FOUND MATCH")
            section_number, section_letter, section_name = match.groups()
            section_number = section_number.strip()
            section_letter = section_letter.strip()
            section_name = section_name.strip()
            #print(f"section_number: '{section_number}'")
            #print(f"section_letter: '{section_letter}'")
            #print(f"section_name: '{section_name}'")

            if section_number == "I":
                if section_letter == "A":
                    return "A", "Data Structures"
                elif section_letter == "B":
                    return "B", "Advanced Data Structures"
                else:
                    print(f"Unable to handle section letter: {section_letter}")
                    print(f"Full match: {match.group(0)}")
                    print(f"Section number: {section_number}")
                    print(f"Section name: {section_name}")
                    return None, None
            elif section_number == "II" or section_number == "I I":
                if section_letter == "A":
                    return "A", "Algorithm Analysis"
                elif section_letter == "B":
                    return "B", "Algorithms"
                else:
                    print(f"Unable to handle section letter: {section_letter}")
                    print(f"Full match: {match.group(0)}")
                    print(f"Section number: {section_number}")
                    print(f"Section name: {section_name}")
                    return None, None
            

            
            return section_letter, section_name.strip()
        
        return None, None
    
    return match.group(1), match.group(2).strip()


def get_page_type(text: str) -> PageType | None:
    if "Computer Science Foundation Exam" in text:
        return PageType.SECTION
    return PageType.QUESTION


def get_section_type(text: str) -> SectionType | None:
    section_letter, section_name = extract_section_info(text)
        
    if section_letter is None:
        print("unable to get section letter")
        return None
    
    if section_name is None:
        print("unable to get section name")
        return None
    
    section_name = " ".join([x.strip() for x in section_name.split(" ") if x.strip() != ""])
    #print(section_name)
    
    if "Advanced Data Structures".lower() in section_name.lower():
        return SectionType.ADVANCED_DATA_STRUCTURES
    elif "Data Structures".lower() in section_name.lower()  :
        return SectionType.BASIC_DATA_STRUCTURES
    elif "Algorithm Analysis".lower() in section_name.lower():
        return SectionType.ALGORITHM_ANALYSIS
    elif "Algorithms".lower() in section_name.lower():
        return SectionType.ALGORITHMS
    return None