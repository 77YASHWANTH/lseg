from flask import Flask, jsonify, send_file , request
import requests
import csv
import os
from io import StringIO

app = Flask(__name__)

# URLs for the previous applications
DATA_APP_URL = os.getenv("stockdata-service")  # Replace with the stock data app's URL
OUTLIER_APP_URL = os.getenv("outlier-service")  # Replace with the outlier app's URL

def save_to_csv(data, file_name):
    """
    Save data to a CSV file.
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Assuming data is a list of dictionaries
    if data and isinstance(data, list):
        # Write headers
        writer.writerow(data[0].keys())
        # Write rows
        for row in data:
            writer.writerow(row.values())

    # Save the output to a file
    output.seek(0)
    with open(file_name, 'w') as f:
        f.write(output.getvalue())

    output.close()
    return file_name

@app.route('/<exchange_name>/<stock_id>/', methods=['GET'])
def get_data_csv(exchange_name, stock_id):
    # Extract query parameters
    date = request.args.get('date')
    no_of_files = request.args.get('noOfFiles', type=int)

    if not date:
        return jsonify({"error": "The 'date' parameter is required."}), 400
    if not no_of_files or no_of_files < 1:
        no_of_files = 1

    try:
        # Send request to the first application
        response = requests.get(
            f"{DATA_APP_URL}/{exchange_name}/{stock_id}/",
            params={"date": date, "noOfFiles": no_of_files}
        )

        if response.status_code != 200:
            return jsonify({"error": f"Error from first app: {response.json()}"}), response.status_code

        data = response.json().get("data", [])

        # Save data to a CSV file
        file_name = f"{exchange_name}_{stock_id}_data.csv"
        save_to_csv(data, file_name)

        # Return the CSV file as an attachment
        return send_file(file_name, as_attachment=True, mimetype='text/csv')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/outliers/<exchange_name>/<stock_id>/', methods=['GET'])
def get_outliers_csv(exchange_name, stock_id):
    # Extract query parameters
    date = request.args.get('date')
    no_of_files = request.args.get('noOfFiles', type=int)

    if not date:
        return jsonify({"error": "The 'date' parameter is required."}), 400
    if not no_of_files or no_of_files < 1:
        no_of_files = 1

    try:
        # Send request to the outlier application
        response = requests.get(
            f"{OUTLIER_APP_URL}/outliers/{exchange_name}/{stock_id}/",
            params={"date": date, "noOfFiles": no_of_files}
        )

        if response.status_code != 200:
            return jsonify({"error": f"Error from outlier app: {response.json()}"}), response.status_code

        data = response.json().get("outliers", [])

        # Save outliers to a CSV file
        file_name = f"{exchange_name}_{stock_id}_outliers.csv"
        save_to_csv(data, file_name)

        # Return the CSV file as an attachment
        return send_file(file_name, as_attachment=True, mimetype='text/csv')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
