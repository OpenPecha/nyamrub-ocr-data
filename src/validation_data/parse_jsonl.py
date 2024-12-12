import csv
import json
import unicodedata
from urllib.parse import urlparse, urlunparse, ParseResult


def parse_image_url(url):
    """clean imag url"""
    parsed_url = urlparse(url)
    stripped_url = ParseResult(parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', '')
    return urlunparse(stripped_url)


def get_writing_type(accept_list):
    """writing type based on the accept list."""
    if 2 in accept_list:
        return "Uchen"
    elif 1 in accept_list:
        return "Non_Uchen"
    else:
        return "Others"


def convert_unicode_to_tibetan(unicode_string):
    return unicodedata.normalize("NFC", unicode_string)


def process_jsonl_entry(entry):
    origin_id = entry.get("id", "")
    image_url = parse_image_url(entry.get("image", ""))
    target = convert_unicode_to_tibetan(entry.get("user_input", ""))
    writing_type = get_writing_type(entry.get("accept", []))
    score = 15

    return {
        "origin_id": origin_id,
        "img_url": image_url,
        "target": target,
        "writing_type": writing_type,
        "score": score
    }


def convert_jsonl_to_csv(jsonl_file, csv_file):
    """Convert JSONL file to a CSV file."""
    with open(jsonl_file, 'r', encoding='utf-8') as infile, open(csv_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ["origin_id", "img_url", "target", "writing_type", "score"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in infile:
            entry = json.loads(line)
            row = process_jsonl_entry(entry)
            writer.writerow(row)


if __name__ == "__main__":
    input_jsonl_file = "data/recheck_b11_to_b16/recheck_ltt_ann_batch11.jsonl"
    output_csv_file = "data/output_csv/ocr_validation_data.csv"
    convert_jsonl_to_csv(input_jsonl_file, output_csv_file)
    print(f"Conversion complete. CSV saved to {output_csv_file}")
