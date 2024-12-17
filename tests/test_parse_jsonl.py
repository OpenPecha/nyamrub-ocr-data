import os
import json
import pytest
import tempfile
import csv

from src.batch_11_to_18.parse_jsonl import parse_image_url, get_writing_type, convert_unicode_to_tibetan, process_jsonl_entry, convert_jsonl_to_csv


def test_parse_image_url():
    test_url = "https://example.com/path/image.jpg?param=value"
    expected = "https://example.com/path/image.jpg"
    assert parse_image_url(test_url) == expected


def test_get_writing_type():
    assert get_writing_type([2]) == "Uchen"
    assert get_writing_type([1]) == "Non_Uchen"
    assert get_writing_type([3]) == "Others"
    assert get_writing_type([]) == "Others"


def test_convert_unicode_to_tibetan():
    test_string = "\u0f60\u0f66"
    normalized = convert_unicode_to_tibetan(test_string)
    assert normalized == test_string


def test_process_jsonl_entry():
    sample_entry = {
        "id": "test123",
        "image": "https://example.com/image.jpg?param=value",
        "user_input": "\u0f60\u0f66",
        "accept": [2]
    }

    processed = process_jsonl_entry(sample_entry)

    assert processed["origin_id"] == "test123"
    assert processed["img_url"] == "https://example.com/image.jpg"
    assert processed["target"] == "\u0f60\u0f66"
    assert processed["writing_type"] == "Uchen"
    assert processed["score"] == 15


def test_convert_jsonl_to_csv():
    with tempfile.TemporaryDirectory() as temp_dir:
        jsonl_file_path = os.path.join(temp_dir, "test_input.jsonl")
        with open(jsonl_file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "id": "test1",
                "image": "https://example.com/image1.jpg",
                "user_input": "\u0f60\u0f66",
                "accept": [2]
            }, f)
            f.write('\n')
            json.dump({
                "id": "test2",
                "image": "https://example.com/image2.jpg",
                "user_input": "\u0f55\u0f72",
                "accept": [1]
            }, f)
            f.write('\n')

        output_csv_path = os.path.join(temp_dir, "output.csv")

        convert_jsonl_to_csv(temp_dir, output_csv_path)
        with open(output_csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            assert len(rows) == 2
            assert rows[0]["origin_id"] == "test1"
            assert rows[0]["writing_type"] == "Uchen"
            assert rows[1]["origin_id"] == "test2"
            assert rows[1]["writing_type"] == "Non_Uchen"


def test_edge_cases():

    sample_entry = {}
    processed = process_jsonl_entry(sample_entry)

    assert processed["origin_id"] == ""
    assert processed["img_url"] == ""
    assert processed["target"] == ""
    assert processed["writing_type"] == "Others"
    assert processed["score"] == 15
