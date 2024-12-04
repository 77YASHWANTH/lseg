FROM python:3.9-slim

WORKDIR /app

COPY app.py /app

RUN pip install flask requests

EXPOSE 5000

ENV stockdata_app_url="http://localhost:5000"  
ENV outlier_app_url="http://localhost:5001"

CMD ["python", "app.py"]
