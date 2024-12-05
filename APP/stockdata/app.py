import os
import csv
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the stock data directory
BASE_PATH = "/stockdata/"

# Helper function to fetch files from the given folder
def fetch_files(exchange_name, stock_id):
    folder_path = os.path.join(BASE_PATH, exchange_name, stock_id)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Directory {folder_path} not found")

    # Get all CSV files in the directory
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    return sorted(files)

# Helper function to parse a CSV file and get 30 consecutive days starting from the date
def parse_csv_file(file_path, start_date):
    parsed_data = []
    end_date = start_date + timedelta(days=30)

    with open(file_path, newline='', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            stock_id = row[0]
            date_value = datetime.strptime(row[1], "%d-%m-%Y")
            price = row[2]

            # If the date is within the 30-day range, add to the data
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
        # Convert the date string to a datetime object
        start_date = datetime.strptime(date, "%d-%m-%Y")

        # Fetch the files from the specified folder
        files = fetch_files(exchange_name, stock_id)

        # If no_of_files is less than 1 or greater than available files, adjust it
        if no_of_files < 1 or no_of_files > len(files):
            no_of_files = len(files)

        # Read the files and extract the data
        data = []
        folder_path = os.path.join(BASE_PATH, exchange_name, stock_id)
        for file_name in files[:no_of_files]:
            file_path = os.path.join(folder_path, file_name)
            data.extend(parse_csv_file(file_path, start_date))

        if not data:
            return jsonify({"message": "No data found for the specified date."}), 404

        return jsonify(data), 200

    except ValueError:
        return jsonify({"error": "Invalid date format. Use dd-mm-yyyy"}), 400
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
