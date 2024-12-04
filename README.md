****STOCKDATAOUTLIER***

# PREREQUISITES

1. Generate the AWS ACCESS KEY & ACCESS ID & UPDATE IN GITHUB -> ACTIONS -> SECRET
2. Create Private ECR registry in AWS & UPDATE ECR_REGISTRY variable in github workflow files .github/workflows*.yml file
3. Create Standard S3 Bucket in Aws
4. Create kubernetes cluster 
5. Install kubectl , eksctl cli

# ENDPOINTS
1. To get 30 days stock price
http://LOADBALANCERURL/EXCHANGENAME/STOCKID/NOOFFILES/DATA - 
EX: http://LOADBALANCERURL/NASDAQ/TSLA/19/05-10-2023

2. To get standard deviation/outliers
.http://LOADBALANCERURL/EXCHANGENAME/STOCKID/outliers/NOOFFILES/DATA - 
EX: http://LOADBALANCERURL/NASDAQ/outliers/TSLA/19/05-10-2023


### SETUP EKS CLUSTER FOR APPLICATION DEPLOYMENTS ####

# Create Cluster
eksctl create cluster --name=stockdata \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b \
                      --without-nodegroup 

# Get List of clusters
```
eksctl get cluster     
```
# Connect with AWS OIDC FOR IRSA

```
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster stockdata \
    --approve
```
# Create Node Group
```
eksctl create nodegroup --cluster=stockdata \
                        --region=us-east-1 \
                        --name=stockdata-ng-public \
                        --node-type=t3.medium \
                        --nodes-min=1 \
                        --nodes-max=2 \
                        --node-volume-size=20 \
                        --ssh-access \
                        --ssh-public-key=yash \
                        --managed \
                        --asg-access \
                        --full-ecr-access \
                        --alb-ingress-access \                                         
```
# Update kubeconfig file 

```
aws eks update-kubeconfig --region us-east-1 --name stockdata
```

# IN KUBERNETES CLUSTER

1.Update the S3 bucket name in stockdata/configmap.yaml
2.Create AWS policy (AWS) providing s3:FullAccess , get the arn
3.Create namespace
``` kubectl create namespace stocks ```

4.Create service account to access s3 in aws from stockdata pod
```
eksctl create iamserviceaccount \
  --cluster=stockdata \
  --namespace=stocks \
  --name=s3-stockdata-access \
  --attach-policy-arn=$policy_arn \
  --override-existing-serviceaccounts \
  --approve

```
eksctl create iamserviceaccount \
  --cluster=stockdata \
  --namespace=stocks \
  --name=s3-stockdata-access \
  --attach-policy-arn=arn:aws:iam::061051251404:policy/s3-stockprice-access \
  --override-existing-serviceaccounts \
  --approve
```

5.Deploy the application 

```
cd CONTAINERIZATION/

kubectl apply -f stockdata/
kubectl apply -f outlier/
kubectl apply -f output/

```

