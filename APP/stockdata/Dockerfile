# Base image
FROM python:3.9-slim

WORKDIR /app

COPY app.py /app

RUN pip install flask boto3

EXPOSE 5000

ENV BUCKET_NAME="your-s3-bucket-name"

CMD ["python", "app.py"]
