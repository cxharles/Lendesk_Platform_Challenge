Part 2: AWS Design

Author: Charles Jatto
My high level AWS design of Part 1: Docker + Github Action will look like this:

Prerequisites:
Version control system (GitHub)
AWS Account 
VPC (Virtual Private Cloud)
ECR (Elastic Container Registry)
EKS (Elastic Kubernetes Service)

SSH Setup and GitHub Integration
I will create an SSH key in my GitHub repository environment. In my IDE (e.g., VS Code), I will run: ssh-keygen -t rsa -C "your-email@gmail.com"
This generates a private and public key. The public key is used to authenticate with the GitHub environment, which can be done by adding a new SSH key in GitHub. This secures GitHub communication from the terminal using commands like: git init --initial-branch=<feature-branch>-actions
The SSH agent will not be needed to push code to GitHub. Instead, I can attach the private key directly with: git config core.sshCommand "ssh -i ~/<path-to-private-key> -F /dev/null"
This attaches the private key to the repository. I can also configure Git with: vi .git/config This allows me to set my Git username and email once, so I don’t have to specify them every time I commit code.

Terraform Configuration:
I will create the following Terraform files and modules for VPC, ECR, and EKS:

main.tf
Specify the provider, host, and cluster CA certificate endpoint.

The provider will be AWS, with the appropriate region.

output.tf
Displays output after resources are created:
Cluster name
Cluster platform version
Cluster version
Cluster status
Cluster configuration
ECR repo URL
ECR repo name

terraform.tf
Configure the backend with an S3 bucket to store state files.

Declare providers, such as:
AWS
Kubernetes (source, version)

variables.tf
Define variables used across resources (e.g., string, integer, count, etc.)

Modules:

VPC Module
I will use a data block to fetch AWS environment info, like the number of Availability Zones in the chosen region.
Create a VPC using Terraform modules with:
source and version
VPC name and CIDR block
Dynamically configured public and private subnets
NAT Gateway enabled (true)
Use count to determine the number of subnets

EKS Module
The eks module will reference VPC outputs as inputs for EKS cluster creation.
Set enable_cluster_admin to true.
Enable EKS add-ons: CoreDNS, kube-proxy, and VPC CNI (use latest versions).
Define EKS Managed Node Groups:
Set instance type, min size, max size, and desired size.
These will form an Auto Scaling Group using EC2, which scales based on app traffic.

ECR Module
Define the repository name in variables.
Set registry scan type, repository type to private, and image tag mutability to mutable (images can be overwritten).
Add appropriate tags.

GitHub Workflow (iac.yml):
Create an iac.yml workflow in the GitHub repository based on the Terraform code above:
Define the workflow name
Setup triggers (e.g., on push or pull request)
Set environment variables for:
AWS Access Key
AWS Secret Access Key
S3 Bucket
AWS Region
EKS Cluster Name
Define jobs:
terraform init, plan, apply, destroy steps

Benefits:
Secure GitHub Integration - SSH-based authentication
Terraform Design - reusable VPC/EKS/ECR modules
Auto-Scalable EKS - dynamic worker node adjustment
Automated CI/CD - GitHub Actions for seamless deployment
