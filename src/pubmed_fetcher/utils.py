import xml.etree.ElementTree as ET
from typing import Optional
from .constants import COMPANY_KEYWORDS, KNOWN_COMPANIES, ACADEMIC_KEYWORDS

def safe_find_text(element: Optional[ET.Element], path: str, default: str = "N/A") -> str:
    """Safely find and extract text from an XML element."""
    if element is None:
        return default
    
    found_elem = element.find(path)
    return found_elem.text if found_elem is not None and found_elem.text else default

def is_company_affiliation(affiliation_text: Optional[str]) -> bool:
    """Check if an affiliation is from a pharmaceutical or biotech company."""
    if not affiliation_text:
        return False

    affiliation_lower = affiliation_text.lower()
    
    has_company_keyword = any(keyword in affiliation_lower for keyword in COMPANY_KEYWORDS)
    has_known_company = any(company in affiliation_lower for company in KNOWN_COMPANIES)
    is_academic = any(keyword in affiliation_lower for keyword in ACADEMIC_KEYWORDS)
    
    return (has_company_keyword or has_known_company) and not is_academic
