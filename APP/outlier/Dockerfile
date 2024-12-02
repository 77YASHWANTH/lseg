FROM python:3.9-slim

WORKDIR /app

COPY app.py /app

RUN pip install flask requests numpy

EXPOSE 5000

ENV stockdata_app_url="http://127.0.0.1:5000" 

CMD ["python", "app.py"]
