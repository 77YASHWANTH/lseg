****STOCKDATAOUTLIER***
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
                        --nodes-max=3 \
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
