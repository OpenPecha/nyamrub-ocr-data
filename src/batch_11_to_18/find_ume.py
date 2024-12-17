import csv
from collections import defaultdict


def read_csv(input_csv):
    work_id_categories = defaultdict(set)
    with open(input_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            work_id = row["work_id"]
            category = row["category"]
            work_id_categories[work_id].add(category)
    return work_id_categories


def filter_valid_work_ids(work_id_categories, valid_categories):
    return [
        work_id
        for work_id, categories in work_id_categories.items()
        if categories.issubset(valid_categories)
    ]


def write_work_ids(output_txt, work_ids):
    with open(output_txt, "w", encoding="utf-8") as file:
        for work_id in work_ids:
            file.write(f"{work_id}\n")


def filter_work_ids(input_csv, output_txt):
    valid_categories = {"ཚུགས་མ་འཁྱུག", "འཁྱུག་ཡིག"}
    work_id_categories = read_csv(input_csv)
    valid_work_ids = filter_valid_work_ids(work_id_categories, valid_categories)

    write_work_ids(output_txt, valid_work_ids)


if __name__ == "__main__":
    input_csv = "data/manuscript_works.csv"
    output_txt = "data/umay_work_ids.txt"
    filter_work_ids(input_csv, output_txt)
