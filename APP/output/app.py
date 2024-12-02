from flask import Flask, request, jsonify, send_file
import os
import requests
import csv
import io

app = Flask(__name__)

# Load the URLs of the previous applications from environment variables
STOCKDATA_APP_URL = os.getenv("STOCKDATA_APP_URL")
OUTLIER_APP_URL = os.getenv("OUTLIER_APP_URL")

if not STOCKDATA_APP_URL or not OUTLIER_APP_URL:
    raise EnvironmentError("Please set the STOCKDATA_APP_URL and OUTLIER_APP_URL environment variables.")

# Function to convert data to CSV
def convert_to_csv(data, columns):
    """Converts a list of dicts to CSV format in memory."""
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=columns)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    output.seek(0)
    return output

@app.route("/<exchange_name>/<stock_id>/<int:no_of_files>/<date>", methods=["GET"])
def fetch_stock_data(exchange_name, stock_id, no_of_files, date):
    try:
        # Request data from the first app
        url = f"{STOCKDATA_APP_URL}/{exchange_name}/{stock_id}/{no_of_files}/{date}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from the stock data application"}), response.status_code
        
        # Convert the data into CSV format
        data = response.json()
        columns = ['date', 'price', 'stock_id']
        csv_output = convert_to_csv(data, columns)

        return send_file(csv_output, mimetype="text/csv", as_attachment=True, download_name="stock_data.csv")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<exchange_name>/<stock_id>/outliers/<int:no_of_files>/<date>", methods=["GET"])
def fetch_outliers_data(exchange_name, stock_id, no_of_files, date):
    try:
        # Request data from the second app
        url = f"{OUTLIER_APP_URL}/{exchange_name}/{stock_id}/{no_of_files}/{date}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from the outlier application"}), response.status_code
        
        # Convert the outlier data into CSV format
        outliers_data = response.json().get('data', [])
        columns = ['stock_id', 'date', 'price', 'mean', 'deviation', 'percentage_deviation']
        csv_output = convert_to_csv(outliers_data, columns)

        return send_file(csv_output, mimetype="text/csv", as_attachment=True, download_name="outliers_data.csv")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
