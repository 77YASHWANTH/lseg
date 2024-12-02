FROM python:3.9-slim

WORKDIR /app

COPY app.py /app

RUN pip install flask requests

EXPOSE 5000

# Set environment variables
ENV stockdata_app_url="http://localhost:5000"  # URL of the first application (App1)
ENV outlier_app_url="http://localhost:5001"  # URL of the second application (App2)

CMD ["python", "app.py"]
