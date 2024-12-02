from flask import Flask, jsonify
import requests
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# URL for the first Flask application (App1)
stockdata_app_url = os.getenv("stockdata_app_url")  

# Helper function to fetch data from App1
def fetch_data_from_app1(exchange_name, stock_id, params):
    try:
        response = requests.get(f"{stockdata_app_url}/{exchange_name}/{stock_id}/", params=params)
        response.raise_for_status()
        return response.json()['data']  # Extract the data field
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to App1: {str(e)}")

# Helper function to calculate outliers
def calculate_outliers(data):
    try:
        prices = [point['Price'] for point in data]
        mean_price = np.mean(prices)
        std_dev = np.std(prices)

        threshold_upper = mean_price + 2 * std_dev
        threshold_lower = mean_price - 2 * std_dev

        outliers = []
        for point in data:
            deviation = point['Price'] - mean_price
            if point['Price'] > threshold_upper or point['Price'] < threshold_lower:
                percent_deviation = abs(deviation) / std_dev * 100
                outliers.append({
                    "StockID": point['StockID'],
                    "Timestamp": point['Date'],
                    "Actual Price": point['Price'],
                    "Mean Price": round(mean_price, 2),
                    "Deviation": round(deviation, 2),
                    "% Deviation": round(percent_deviation, 2)
                })

        return outliers
    except Exception as e:
        raise Exception(f"Error calculating outliers: {str(e)}")

@app.route('/outliers/<exchange_name>/<stock_id>/', methods=['GET'])
def get_outliers(exchange_name, stock_id):
    # Validate query parameters
    date_param = request.args.get('date')
    no_of_files = request.args.get('noOfFiles', type=int)

    if not date_param:
        return jsonify({"error": "The 'date' parameter is required."}), 400
    if not no_of_files or no_of_files < 1:
        no_of_files = 1

    try:
        # Fetch data from App1
        params = {"date": date_param, "noOfFiles": no_of_files}
        data = fetch_data_from_app1(exchange_name, stock_id, params)

        # Convert data to a DataFrame for easier processing
        df = pd.DataFrame(data)

        # Validate and parse data structure
        if df.empty or len(df) < 30:
            return jsonify({"error": "Insufficient data points for analysis. At least 30 data points required."}), 400

        # Calculate outliers
        outliers = calculate_outliers(data)

        if not outliers:
            return jsonify({"message": "No outliers found."}), 200

        return jsonify({"outliers": outliers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
