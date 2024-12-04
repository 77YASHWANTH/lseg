****STOCKDATAOUTLIER***

# PREREQUISITES

1. Generate the AWS ACCESS KEY & ACCESS ID & UPDATE IN GITHUB -> ACTIONS -> SECRET
2. Create Private ECR registry in AWS & UPDATE ECR_REGISTRY variable in github workflow files .github/workflows*.yml file
3. Create Standard S3 Bucket in Aws
4. Create kubernetes cluster 

# PIPELINE

1.Update the AWS_ACCE

#REQUEST ENDPOINTS


/
1



###SETUP EKS CLUSTER FOR APPLICATION DEPLOYMENTS ####

# Create Cluster
eksctl create cluster --name=stockprice \
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
    --cluster stockprice \
    --approve
```
eksctl create nodegroup --cluster=stockprice \
                        --region=us-east-1 \
                        --name=stockprice-ng-private1 \
                        --node-type=t3.medium \
                        --nodes-min=1 \
                        --nodes-max=2 \
                        --node-volume-size=20 \
                        --ssh-access \
                        --ssh-public-key=kube-demo \
                        --managed \
                        --asg-access \
                        --full-ecr-access \
                        --alb-ingress-access \
                        --node-private-networking                       
```


#Update kubeconfig file 

```
aws eks update-kubeconfig --region us-east-1 --name stockprice
```

#IN KUBERNETES CLUSTER

Update the S3 bucket name in stockdata/configmap.yaml


```
cd CONTAINERIZATION


kubectl create namespace stocks
kubectl apply -f stockdata/
kubectl apply -f outlier/
kubectl apply -f output/


```

