# PubMed Fetcher
PubMed Fetcher is a Python tool for fetching and processing PubMed articles based on a given query. It allows you to search for articles, extract relevant details, and save the results to a CSV file.

## Features

- Fetch PubMed IDs for a given query.
- Extract details from PubMed articles, including title, publication date, non-academic authors, and company affiliations.
- Save the extracted details to a CSV file.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Pammi-Dharewa/pubmed-fetcher.git
    cd pubmed-fetcher
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

To fetch and process PubMed articles, run the `main.py` script with the desired query and output file:

```sh
python -m src.pubmed_fetcher.main "your_query" --output output_file.csv
```

## Project Structure

```markdown
pubmed-fetcher/
│
├── src/
│   ├── pubmed_fetcher/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── pubmed.py
│   │   └── utils.py
│
├── [README.md](http://_vscodecontentref_/1)
├── requirements.txt
└── [pubmed_fetcher.log](http://_vscodecontentref_/2)
```

python -m src.pubmed_fetcher.main "vaccine" --output papers.csv


License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

Contact
For any questions or suggestions, please contact 'pammidharewa31@gmail.com'.




