from flask import Flask, request, jsonify
import os
import boto3
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the AWS S3 bucket name from the environment variable
BUCKET_NAME = os.getenv("BUCKET_NAME")

if not BUCKET_NAME:
    raise EnvironmentError("Please set the BUCKET_NAME environment variable.")

# AWS S3 client
s3_client = boto3.client("s3")


def fetch_files_from_s3(exchange_name, stock_id, no_of_files):
    """
    Fetch files from S3 bucket based on the key structure.
    """
    prefix = f"{exchange_name}/{stock_id}/"
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    files = response.get("Contents", [])

    if not files:
        return []

    # Sort files by last modified date in descending order
    sorted_files = sorted(files, key=lambda x: x["LastModified"], reverse=True)
    file_keys = [file["Key"] for file in sorted_files]

    # Return requested number of files or all available if no_of_files is invalid
    if no_of_files < 1 or no_of_files > len(file_keys):
        return file_keys
    return file_keys[:no_of_files]


def parse_csv_file(file_content, start_date):
    """
    Parse the CSV file and return data for 30 consecutive days from the start_date.
    """
    parsed_data = []
    end_date = start_date + timedelta(days=30)

    csv_reader = csv.reader(file_content.splitlines())
    for row in csv_reader:
        stock_id = row[0]
        date_value = datetime.strptime(row[1], "%d-%m-%Y")
        price = row[2]

        if start_date <= date_value < end_date:
            parsed_data.append({
                "stock_id": stock_id,
                "date": date_value.strftime("%d-%m-%Y"),
                "price": price
            })

    return parsed_data


@app.route("/<exchange_name>/<stock_id>/<int:no_of_files>/<date>", methods=["GET"])
def get_stock_data(exchange_name, stock_id, no_of_files, date):
    try:
        # Convert date to datetime object
        start_date = datetime.strptime(date, "%d-%m-%Y")

        # Fetch files from S3
        files = fetch_files_from_s3(exchange_name, stock_id, no_of_files)
        if not files:
            return jsonify({"error": "No files found in the S3 bucket"}), 404

        data = []
        for file_key in files:
            obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            file_content = obj["Body"].read().decode("utf-8")
            data.extend(parse_csv_file(file_content, start_date))

        return jsonify(data), 200

    except ValueError:
        return jsonify({"error": "Invalid date format. Use dd-mm-yyyy"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
