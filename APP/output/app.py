from flask import Flask, request, jsonify, send_file
import os
import requests
import csv
import tempfile

app = Flask(__name__)

STOCKDATA_APP_URL = os.getenv("STOCKDATA_APP_URL")
OUTLIER_APP_URL = os.getenv("OUTLIER_APP_URL")

if not STOCKDATA_APP_URL or not OUTLIER_APP_URL:
    raise EnvironmentError("Please set the STOCKDATA_APP_URL and OUTLIER_APP_URL environment variables.")

def write_to_temp_csv(data, columns):
    try:
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
        csv_writer = csv.DictWriter(temp_file, fieldnames=columns)
        csv_writer.writeheader()
        csv_writer.writerows(data)
        temp_file.close()  # Ensure data is written before returning
        return temp_file.name
    except Exception as e:
        raise ValueError(f"Error generating CSV: {e}")

# Endpoint 1: Fetch stock data and return it as a CSV attachment
@app.route("/<exchange_name>/<stock_id>/<int:no_of_files>/<date>", methods=["GET"])
def fetch_stock_data(exchange_name, stock_id, no_of_files, date):
    try:
        # Fetch data from the STOCKDATA app
        url = f"{STOCKDATA_APP_URL}/{exchange_name}/{stock_id}/{no_of_files}/{date}"
        response = requests.get(url)

        # Check for valid response
        if response.status_code != 200:
            return jsonify({"error": "Invalid data"}), response.status_code

        data = response.json()

        # Verify expected format
        if not isinstance(data, list) or not all("date" in item and "price" in item and "stock_id" in item for item in data):
            return jsonify({"error": "Invalid data format"}), 400

        # Write data to a temporary CSV file
        columns = ["date", "price", "stock_id"]
        temp_file_path = write_to_temp_csv(data, columns)

        return send_file(temp_file_path, mimetype="text/csv", as_attachment=True, download_name="stock_data.csv")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint 2: Fetch outliers data and return it as a CSV attachment
@app.route("/<exchange_name>/<stock_id>/outliers/<int:no_of_files>/<date>", methods=["GET"])
def fetch_outliers_data(exchange_name, stock_id, no_of_files, date):
    try:
        # Fetch data from the OUTLIER app
        url = f"{OUTLIER_APP_URL}/{exchange_name}/{stock_id}/{no_of_files}/{date}"
        response = requests.get(url)

        # Check for valid response
        if response.status_code != 200:
            return jsonify({"error": "Invalid data"}), response.status_code

        data = response.json()

        # Verify expected format
        if not isinstance(data, list) or not all(
            {"date", "deviation_from_mean", "mean", "outlier", "percentage_deviation", "price", "stock_id"}.issubset(item.keys())
            for item in data
        ):
            return jsonify({"error": "Invalid data format"}), 400

        # Write data to a temporary CSV file
        columns = ["stock_id", "date", "price", "mean", "deviation_from_mean", "percentage_deviation", "outlier"]
        temp_file_path = write_to_temp_csv(data, columns)

        return send_file(temp_file_path, mimetype="text/csv", as_attachment=True, download_name="outliers_data.csv")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
