# Microservices Deployment on AWS EKS

A production-grade microservices application deployed to AWS EKS using Terraform and Kubernetes. This project demonstrates Infrastructure as Code, container orchestration, and cloud-native DevOps practices.

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────┐
│   Frontend      │────▶ │ API Gateway  │
│   (Nginx)       │      │  (Flask)     │
└─────────────────┘      └──────┬───────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              ┌─────────────┐        ┌──────────────┐
              │User Service │        │Product Service│
              │  (Flask)    │        │   (Flask)    │
              └─────────────┘        └──────────────┘
```

## 🚀 Tech Stack

- **Application:** Python Flask, Nginx
- **Containerization:** Docker
- **Orchestration:** Kubernetes
- **Infrastructure:** AWS EKS, Terraform
- **Registry:** Docker Hub

## 📁 Project Structure

```
microservices/
├── project/                    # Application source code
│   ├── user-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── product-service/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── api-gateway/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
│       ├── index.html
│       ├── style.css
│       ├── app.js
│       └── Dockerfile
├── manifests/                  # Kubernetes manifests
│   ├── user-manifest/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── product-manifest/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── gateway-manifest/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── frontend-manifest/
│       ├── deployment.yaml
│       └── service.yaml
├── terraform-eks/              # Infrastructure as Code
│   ├── provider.tf
│   ├── variables.tf
│   ├── vpc.tf
│   ├── iam.tf
│   ├── security-groups.tf
│   ├── eks.tf
│   └── outputs.tf
├── docker/
│   └── build-all.sh           # Build script for all services
├── .gitignore
└── README.md
```

## 🛠️ Prerequisites

- Docker Desktop installed
- AWS CLI configured
- kubectl installed
- Terraform >= 1.0
- AWS account with appropriate permissions
- Docker Hub account

## 📦 Quick Start

### Option 1: Build All Services at Once

```bash
cd docker
./build-all.sh
```

### Option 2: Build Services Individually

```bash
# User Service
cd project/user-service
docker build -t akila1908/user-service:v1 .
docker push akila1908/user-service:v1

# Product Service
cd ../product-service
docker build -t akila1908/product-service:v1 .
docker push akila1908/product-service:v1

# API Gateway
cd ../api-gateway
docker build -t akila1908/api-gateway:v1 .
docker push akila1908/api-gateway:v1

# Frontend
cd ../frontend
docker build -t akila1908/frontend:v1 .
docker push akila1908/frontend:v1
```

## 🧪 Local Testing with Minikube

```bash
# Start Minikube
minikube start

# Deploy all services
kubectl apply -f manifests/user-manifest/
kubectl apply -f manifests/product-manifest/
kubectl apply -f manifests/gateway-manifest/
kubectl apply -f manifests/frontend-manifest/

# Check deployment status
kubectl get pods
kubectl get svc

# Access the application
minikube service frontend
```

## ☁️ AWS Deployment

### 1. Configure AWS CLI

```bash
aws configure
# Enter your Access Key, Secret Key, Region (us-east-1), Output format (json)

# Verify configuration
aws sts get-caller-identity
```

### 2. Deploy Infrastructure with Terraform

```bash
cd terraform-eks/

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply configuration (creates ~28 resources)
terraform apply
```

**What gets created:**
- VPC with public and private subnets (2 AZs)
- EKS cluster with managed control plane
- 2x t3.medium worker nodes
- IAM roles for EKS cluster and nodes
- Security groups for cluster communication
- NAT Gateway and Internet Gateway
- Application Load Balancers (via Kubernetes)

### 3. Connect kubectl to EKS

```bash
# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name microservices-dev

# Verify connection
kubectl get nodes
```

### 4. Deploy Application to EKS

```bash
# Deploy all services
kubectl apply -f manifests/user-manifest/
kubectl apply -f manifests/product-manifest/
kubectl apply -f manifests/gateway-manifest/
kubectl apply -f manifests/frontend-manifest/

# Wait for pods to start
kubectl get pods -w

# Get LoadBalancer URLs (wait 2-3 minutes for provisioning)
kubectl get svc
```

### 5. Access Your Application

```bash
# Get the frontend LoadBalancer URL
kubectl get svc frontend

# Visit the EXTERNAL-IP in your browser
# Example: http://a5aa261583f554bada098115d036d60b-1247571435.us-east-1.elb.amazonaws.com
```

## 🧹 Cleanup

**⚠️ CRITICAL: Follow this order to avoid orphaned resources and charges!**

```bash
# Step 1: Delete Kubernetes resources (including LoadBalancers)
kubectl delete -f manifests/user-manifest/
kubectl delete -f manifests/product-manifest/
kubectl delete -f manifests/gateway-manifest/
kubectl delete -f manifests/frontend-manifest/

# Step 2: Verify LoadBalancers are deleted (wait 2-3 minutes)
kubectl get svc
# Should only show: kubernetes ClusterIP

# Step 3: Destroy Terraform infrastructure
cd terraform-eks/
terraform destroy
# Type 'yes' to confirm

# Step 4: Verify cleanup in AWS Console
# Check: EC2 → Load Balancers (should be empty)
# Check: EKS → Clusters (should be empty)
```

## 🎯 Key Features

✅ Infrastructure as Code with Terraform  
✅ Containerized microservices architecture  
✅ Kubernetes orchestration on AWS EKS  
✅ Multi-AZ deployment for high availability  
✅ LoadBalancer for external access  
✅ Internal ClusterIP for backend services  
✅ Production-ready security groups and IAM roles  
✅ Scalable architecture with replica sets  

## 📝 Services Overview

| Service | Type | Replicas | Port | Purpose |
|---------|------|----------|------|---------|
| Frontend | LoadBalancer | 3 | 80 | Web UI (Nginx) |
| API Gateway | LoadBalancer | 2 | 8080 | Request routing (Flask) |
| User Service | ClusterIP | 2 | 5000 | User management (Flask) |
| Product Service | ClusterIP | 2 | 5001 | Product catalog (Flask) |

## 🔧 Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### LoadBalancer stuck in pending
```bash
# Check service events
kubectl describe svc frontend

# Verify security groups allow traffic
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=<your-vpc-id>"
```

### Can't access application
```bash
# Verify LoadBalancer is provisioned
kubectl get svc

# Test API Gateway directly
curl http://<api-gateway-lb-url>:8080/status
```

## 📚 Lessons Learned

1. **Test locally first** - Minikube saves AWS costs and debugging time
2. **Client-side vs server-side execution** - Browser JavaScript needs public URLs, not localhost
3. **Docker image versioning** - Always rebuild and push after code changes
4. **Cleanup order matters** - Delete Kubernetes resources before Terraform to avoid orphaned LoadBalancers
5. **Infrastructure as Code** - Terraform makes environments reproducible and disaster recovery simple

## 🔗 Related Resources

- **Blog Post:** [Deploying Microservices to AWS EKS: A Real DevOps Journey](https://medium.com/@akila98sri/deploying-microservices-to-aws-eks-a-real-devops-journey-50648c67dc1e)


## 👤 Author

**Akila Sri**
- Medium: [@akila98sri](https://medium.com/@akila98sri)
- LinkedIn: [LinkedIn URL](www.linkedin.com/in/akilandeshwari-srinivasan)
- Email: akila98sri@gmail.com

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- AWS EKS Documentation
- Terraform AWS Provider
- Kubernetes Documentation
- DevOps community for best practices

---

**⭐ If you found this project helpful, please consider giving it a star!**

**💬 Have questions? Open an issue or reach out on LinkedIn!**