from flask import Flask, request, jsonify , request
import boto3
import pandas as pd
import os
from datetime import datetime
import io

app = Flask(__name__)

# S3 Configuration
BUCKET_NAME = os.getenv("bucketname")

# Initialize S3 client
s3_client = boto3.client('s3')

def fetch_files_from_s3(exchange_name, stock_id, max_files):
    """
    Fetch CSV files from the specified folder in the S3 bucket.
    """
    try:
        folder_path = f"{exchange_name}/{stock_id}/"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_path)

        if 'Contents' not in response:
            return []

        files = [file['Key'] for file in response['Contents'] if file['Key'].endswith('.csv')]

        # Limit the number of files to the specified max_files
        max_files = max(1, min(max_files, len(files)))  # Ensure 1 <= max_files <= number of files in bucket
        return files[:max_files]
    except Exception as e:
        raise Exception(f"Error fetching files from S3: {str(e)}")

def process_file_from_s3(file_key, date_param):
    """
    Process a single file from S3 and retrieve 30 consecutive rows based on the date_param.
    """
    try:
        # Fetch the file from S3
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
        data = obj['Body'].read().decode('utf-8')

        # Load the file into a DataFrame
        df = pd.read_csv(io.StringIO(data), header=None, names=["StockID", "Date", "Price"])
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

        # Filter for the specified date and retrieve 30 consecutive rows
        date_param = datetime.strptime(date_param, '%d-%m-%Y')
        date_index = df[df['Date'] == date_param].index

        if len(date_index) == 0:
            return None  # Date not found in the file

        start_idx = date_index[0]
        sampled_data = df.iloc[start_idx:start_idx+30]

        return sampled_data.to_dict(orient='records')
    except Exception as e:
        raise Exception(f"Error processing file {file_key}: {str(e)}")

@app.route('/<exchange_name>/<stock_id>/', methods=['GET'])
def get_stock_data(exchange_name, stock_id):
    # Validate and retrieve query parameters
    date_param = request.args.get('date')
    no_of_files = request.args.get('noOfFiles', type=int)

    if not date_param:
        return jsonify({"error": "The 'date' parameter is required."}), 400
    if not no_of_files or no_of_files < 1:
        no_of_files = 1

    try:
        # Fetch files from S3
        files = fetch_files_from_s3(exchange_name, stock_id, no_of_files)

        if not files:
            return jsonify({"error": "No files found in the specified folder."}), 404

        results = []
        for file_key in files:
            sampled_data = process_file_from_s3(file_key, date_param)
            if sampled_data:
                results.extend(sampled_data)

        if not results:
            return jsonify({"message": "No data found for the specified date."}), 404

        return jsonify({"data": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
