#!/bin/bash

#Validating is bucket name is passed as argument
if [ -z "$1" ]; then
  echo "Usage: $0 <bucket-name>"
  exit 1
fi

BUCKET_NAME=$1

aws s3 cp s3://$BUCKET_NAME/ /stockdata/ --recursive

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "S3 bucket contents saved to s3_bucket_list.json"
else
  echo "Failed to list S3 bucket contents"
  exit 1
fi
