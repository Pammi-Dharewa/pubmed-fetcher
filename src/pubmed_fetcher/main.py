import typer
from pubmed_fetcher.pubmed import fetch_papers, fetch_paper_details, save_to_csv

def process_papers(query: str, max_results: int, output: str) -> None:
    """Fetch and process PubMed papers."""
    pubmed_ids = fetch_papers(query, max_results)
    papers = fetch_paper_details(pubmed_ids)

    if papers:
        save_to_csv(papers, output)
    else:
        print("No papers matched the criteria.")

def main(query: str, output: str, max_results: int = 100) -> None:
    """CLI for fetching and filtering PubMed papers."""
    process_papers(query, max_results, output)

if __name__ == "__main__":
    typer.run(main)
