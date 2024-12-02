#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 061051251404.dkr.ecr.us-east-1.amazonaws.com

docker build -t stockdata .
docker tag stockdata:latest 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/stockdata:5.0
docker push 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/stockdata:5.0