"""CSV and JSON export."""
import csv
import json
from pathlib import Path


def export_records(records, output_dir: str, base_name: str, output_format: str = "both"):
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [record.to_dict() for record in records]
    written = []
    if output_format in {"csv", "both"}:
        csv_path = out_dir / f"{base_name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            columns = ["text", "author", "tags", "source_url", "scraped_at"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                row = dict(row)
                row["tags"] = ", ".join(row["tags"])
                writer.writerow(row)
        written.append(csv_path)
    if output_format in {"json", "both"}:
        json_path = out_dir / f"{base_name}.json"
        with json_path.open("w", encoding="utf-8") as file:
            json.dump(rows, file, ensure_ascii=False, indent=2)
        written.append(json_path)
    return written
