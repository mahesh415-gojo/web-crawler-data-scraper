"""Controller joining crawler service and export service."""
from datetime import datetime
from services.crawler import crawl
from services.exporter import export_records


class ScraperController:
    def run(self, url: str, pages: int, workers: int, mode: str,
            timeout: int, delay: float, output_format: str, output_dir: str):
        records = crawl(
            start_url=url, pages=pages, workers=workers, mode=mode,
            timeout=timeout, delay=delay,
        )
        base_name = "quotes_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        paths = export_records(records, output_dir, base_name, output_format)
        return records, paths
