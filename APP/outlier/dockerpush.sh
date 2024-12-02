#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 061051251404.dkr.ecr.us-east-1.amazonaws.com

docker build -t outlier:1.0 .
docker tag outlier:1.0 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/outliers:8.0
docker push 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/outliers:8.0


#docker run -d -p 5000:5000 --env stockdata_app_url="http://xyz.com" outlier:1.0