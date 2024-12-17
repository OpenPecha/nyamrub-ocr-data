import os
import boto3
import csv
import json
from multiprocessing import Pool


def upload_to_s3(file_path, bucket_name, s3_prefix):
    s3_client = boto3.client('s3')
    try:
        s3_key = f"{s3_prefix}{os.path.basename(file_path)}"
        s3_client.upload_file(file_path, bucket_name, s3_key)
        img_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
        print(f"Uploaded file: {file_path} to S3 as {img_url}")

        return img_url
    except Exception as e:
        print(f"Error uploading file {file_path} to S3: {e}")
        return None


def load_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def image_exists(image_name, images_dir):
    image_path = os.path.join(images_dir, image_name)
    return os.path.exists(image_path)


def write_to_csv(csv_output_path, csv_fields, csv_rows):
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        csv_writer.writeheader()
        csv_writer.writerows(csv_rows)
    print(f"CSV file saved at: {csv_output_path}")


def process_image(item, bucket_name, s3_prefix, images_dir):
    image_name = item['image_name']
    text = item['text']

    if image_exists(image_name, images_dir):
        image_path = os.path.join(images_dir, image_name)
        img_url = upload_to_s3(image_path, bucket_name, s3_prefix)

        if img_url:
            return {
                "origin_id": image_name,
                "img_url": img_url,
                "target": text,
                "writing_type": "Non_Uchen",
                "score": 15
            }
    return None


def process_images(json_data, bucket_name, s3_prefix, images_dir):
    with Pool() as pool:
        results = pool.starmap(process_image, [(item, bucket_name, s3_prefix, images_dir) for item in json_data])

    return [result for result in results if result is not None]


def main():
    bucket_name = "monlam.ai.ocr"
    s3_prefix = "ume_line_images/"

    json_file_path = "data/ume_data/image_coordinates_and_text.json"
    images_dir = "data/ume_data/line_segmented_images"
    csv_output_path = "data/ume_data/ume_output.csv"

    csv_fields = ["origin_id", "img_url", "target", "writing_type", "score"]
    json_data = load_json(json_file_path)
    csv_rows = process_images(json_data, bucket_name, s3_prefix, images_dir)

    write_to_csv(csv_output_path, csv_fields, csv_rows)


if __name__ == "__main__":
    main()
