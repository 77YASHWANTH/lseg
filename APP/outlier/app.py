import os
import requests
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

app.config["DEBUG"] = True

STOCKDATA_APP_URL = os.getenv("STOCKDATA_APP_URL")

if not STOCKDATA_APP_URL:
    raise EnvironmentError("Please set the STOCKDATA_APP_URL environment variable.")

def calculate_deviation(data_points):
    """
    Calculate mean, standard deviation, and deviations from the mean for the data points.
    """
    try:
        prices = [float(item["price"]) for item in data_points]
        mean = np.mean(prices)
        std_dev = np.std(prices)

        results = []
        for item in data_points:
            price = float(item["price"])
            deviation_from_mean = price - mean
            percentage_deviation = (deviation_from_mean / mean) * 100
            is_outlier = abs(deviation_from_mean) > 2 * std_dev  # check if it's more than 2 standard deviations

            # Explicitly convert the boolean to integer (0/1) or string ("true"/"false")
            results.append({
                "date": item["date"],
                "price": item["price"],
                "stock_id": item["stock_id"],
                "mean": round(mean, 2),
                "deviation_from_mean": round(deviation_from_mean, 2),
                "percentage_deviation": round(percentage_deviation, 2),
                "outlier": 1 if is_outlier else 0  # Convert bool to integer (1 for True, 0 for False)
            })

        return results

    except Exception as e:
        app.logger.error(f"Error calculating deviation: {e}")
        raise


@app.route("/<exchange_name>/<stock_id>/<int:no_of_files>/<date>", methods=["GET"])
def get_stock_data_with_deviation(exchange_name, stock_id, no_of_files, date):
    try:
        url = f"{STOCKDATA_APP_URL}/{exchange_name}/{stock_id}/{no_of_files}/{date}"

        # Make a request to the first application
        response = requests.get(url)

        if response.status_code != 200:
            app.logger.error(f"Failed to fetch data from the stock data application: {response.text}")
            return jsonify({"error": "Failed to fetch data from the stock data application"}), 500

        data_points = response.json()

        # Calculate deviations for the data points
        result = calculate_deviation(data_points)

        return jsonify(result), 200

    except Exception as e:
        app.logger.error(f"Error in get_stock_data_with_deviation: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
