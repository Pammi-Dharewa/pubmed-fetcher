import requests
import xml.etree.ElementTree as ET
import time
import logging
import pandas as pd
from typing import List, Dict, Optional
from .utils import safe_find_text, is_company_affiliation

# Configure Logging
logging.basicConfig(
    filename="pubmed_fetcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def fetch_papers(query: str, max_results: int = 100) -> List[str]:
    """Fetches PubMed IDs for a given query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "esearchresult" not in data:
            logging.error("Unexpected API response format: 'esearchresult' key missing")
            return []
            
        id_list = data["esearchresult"].get("idlist", [])
        logging.info(f"Found {len(id_list)} PubMed IDs for query: {query}")
        return id_list

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching PubMed data: {e}")
        return []

def parse_pubmed_article(article: ET.Element) -> Optional[Dict[str, str]]:
    """Extracts relevant details from a PubMed article XML element."""
    pmid = safe_find_text(article, ".//PMID")
    title_text = safe_find_text(article, ".//ArticleTitle")
    pub_date_text = safe_find_text(article, ".//PubDate/Year")

    company_authors = []
    company_affiliations = []

    authors = article.findall(".//Author")
    for author in authors:
        author_name = f"{safe_find_text(author, 'ForeName')} {safe_find_text(author, 'LastName')}".strip()
        affiliations = author.findall(".//Affiliation")

        for affiliation_elem in affiliations:
            if affiliation_elem is not None and affiliation_elem.text:
                affiliation_text = affiliation_elem.text
                if is_company_affiliation(affiliation_text):
                    company_affiliations.append(affiliation_text)
                    company_authors.append(author_name)

    return {
        "PubmedID": pmid,
        "Title": title_text,
        "Publication Date": pub_date_text,
        "Non-academic Author(s)": "; ".join(company_authors) or "N/A",
        "Company Affiliation(s)": "; ".join(company_affiliations) or "N/A",
    } if company_affiliations else None

def fetch_paper_details(pubmed_ids: List[str], batch_size: int = 50) -> List[Dict[str, str]]:
    """Fetches details for given PubMed IDs."""
    papers = []

    for i in range(0, len(pubmed_ids), batch_size):
        batch_ids = pubmed_ids[i:i+batch_size]
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pubmed", "id": ",".join(batch_ids), "retmode": "xml"}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.text)

            for article in root.findall(".//PubmedArticle"):
                paper_info = parse_pubmed_article(article)
                if paper_info:
                    papers.append(paper_info)

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching details: {e}")
            continue
        
        time.sleep(0.5)

    return papers

def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    """Saves extracted papers to a CSV file."""
    if not papers:
        print("No papers found.")
        return
    
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Saved {len(papers)} papers to {filename}")
