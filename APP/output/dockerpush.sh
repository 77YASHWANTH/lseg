#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 061051251404.dkr.ecr.us-east-1.amazonaws.com

docker build -t output .
docker tag output:latest 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/:latest
docker push 061051251404.dkr.ecr.us-east-1.amazonaws.com/stockdata/:latest