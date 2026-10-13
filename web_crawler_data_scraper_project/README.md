# Web Crawler & Data Scraper — Data Engineering Project

A portfolio-ready Python project demonstrating:
- MVC-style separation (models, services, controllers, CLI entry point)
- Concurrent scraping with `ThreadPoolExecutor`
- Requests + BeautifulSoup for ordinary HTML and Selenium for JavaScript-rendered pages
- CSV and JSON export
- Configurable user-agent rotation and request throttling
- CAPTCHA / access-denied detection with safe stop-and-review behavior
- Logging, retries, input validation, and API testing notes for Postman

## Responsible use
Use this project only on websites you own or are explicitly allowed to scrape. Check the site's Terms of Service and `robots.txt`, use low concurrency, and prefer an official API when available. User-agent rotation is for identifying ordinary client requests, **not** for bypassing blocks. CAPTCHA detection does not solve or evade CAPTCHAs; the scraper stops/flags the page for manual review.

## 1. Requirements
- Python 3.10+
- Chrome or Chromium installed (for Selenium mode)
- Internet access for the demo target

## 2. Setup

```bash
# Windows PowerShell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Selenium Manager normally downloads/manages the matching browser driver automatically. If your environment blocks this, install a compatible ChromeDriver and put it on PATH.

## 3. Run the demo

The default demo uses `https://quotes.toscrape.com/js/`, a practice site intended for scraping exercises.

```bash
python main.py --url https://quotes.toscrape.com/js/ --pages 3 --mode selenium --format both
```

Try the Requests path too:

```bash
python main.py --url https://quotes.toscrape.com/ --pages 3 --mode requests --format both
```

Output is written to `output/quotes_YYYYMMDD_HHMMSS.csv` and `.json`.

### Arguments
- `--url`: starting URL
- `--pages`: maximum number of paginated pages to visit
- `--mode`: `requests`, `selenium`, or `auto` (Requests first, Selenium fallback when little/no data is found)
- `--workers`: number of concurrent page tasks (default 3; keep low)
- `--delay`: minimum delay in seconds before each page fetch (default 1.0)
- `--format`: `csv`, `json`, or `both`
- `--output`: output directory (default `output`)
- `--timeout`: request/browser timeout in seconds (default 20)

## 4. Project structure

```text
web_crawler_data_scraper/
├── main.py
├── requirements.txt
├── README.md
├── config.py
├── models/
│   ├── __init__.py
│   └── quote.py
├── services/
│   ├── __init__.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── crawler.py
│   └── exporter.py
├── controllers/
│   ├── __init__.py
│   └── scraper_controller.py
├── utils/
│   ├── __init__.py
│   ├── logging_config.py
│   └── safety.py
├── tests/
│   └── test_parser.py
└── postman/
    └── README.md
```

## 5. MVC mapping
- **Model:** `models/quote.py` defines the structured record.
- **View:** CLI output and CSV/JSON files are the user-facing output.
- **Controller:** `controllers/scraper_controller.py` coordinates the run.
- **Services:** fetching, parsing, crawling, and exporting are isolated for maintainability.

## 6. Data schema
Each record contains:
- `text`: quote text
- `author`: author name
- `tags`: list of tags
- `source_url`: page URL where it was found
- `scraped_at`: UTC timestamp

## 7. CAPTCHA and blocked-page behavior
If a page looks like a CAPTCHA or access-denied page, the fetcher raises a `BlockedPageError`. The worker logs the event and skips that page. It does not attempt to solve a CAPTCHA, rotate identities to defeat a block, or circumvent access controls.

## 8. Postman / API testing
This project is a web scraper, not an HTTP API server, so Postman cannot directly test a local API endpoint unless you add one. You can use Postman to:
1. Send `GET https://quotes.toscrape.com/` and inspect the response code/body.
2. Compare the raw HTML with the records extracted by the scraper.
3. Test any official API endpoint of a target site by sending sample requests and validating the response schema.
See `postman/README.md`.

## 9. Tests

```bash
python -m unittest discover -s tests -v
```

## 10. Resume description (accurate after you run and understand it)
Built a concurrent Python web scraper using Requests, BeautifulSoup, and Selenium for JavaScript-rendered pages. Added structured CSV/JSON exports, configurable throttling, rotating standard User-Agent headers, CAPTCHA/access-denied detection, logging, and an MVC-style architecture. Tested parsing with unit tests and validated HTTP responses using Postman.

Do not claim features you have not run or tested on your own machine.
