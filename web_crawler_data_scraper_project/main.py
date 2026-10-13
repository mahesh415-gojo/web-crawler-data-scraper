"""CLI entry point."""
import argparse
from config import DEFAULT_URL, DEFAULT_PAGES, DEFAULT_WORKERS, DEFAULT_DELAY_SECONDS, DEFAULT_TIMEOUT_SECONDS
from controllers.scraper_controller import ScraperController
from utils.logging_config import configure_logging
from utils.safety import validate_url


def parse_args():
    parser = argparse.ArgumentParser(description="Concurrent structured web scraper")
    parser.add_argument("--url", default=DEFAULT_URL, help="Starting URL")
    parser.add_argument("--pages", type=int, default=DEFAULT_PAGES, help="Number of practice-site pages")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Concurrent page workers; keep low")
    parser.add_argument("--mode", choices=("requests", "selenium", "auto"), default="auto")
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY_SECONDS, help="Minimum delay per page fetch")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--format", dest="output_format", choices=("csv", "json", "both"), default="both")
    parser.add_argument("--output", default="output", help="Output directory")
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging()
    try:
        url = validate_url(args.url)
        controller = ScraperController()
        records, paths = controller.run(
            url=url, pages=args.pages, workers=args.workers, mode=args.mode,
            timeout=args.timeout, delay=args.delay,
            output_format=args.output_format, output_dir=args.output,
        )
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(2)
    print(f"\nScraping complete. Records collected: {len(records)}")
    for path in paths:
        print(f"Saved: {path.resolve()}")


if __name__ == "__main__":
    main()
