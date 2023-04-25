module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-cluster"
  cluster_version = "1.25"
  subnet_ids      = module.vpc.private_subnets
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  vpc_id = module.vpc.vpc_id
  eks_managed_node_groups = {
    one = {
      name = "node-group-1"

      instance_types = ["t2.medium"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }
   cluster_addons = {
    coredns = {
        most_recent = true
    }
    kube-proxy = {
        most_recent = true
    }
    vpc-cni = { 
        most_recent = true
    }
  }
}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "EKS-Terra-VPC"
  cidr = "10.0.0.0/16"

  azs                = ["us-east-1a", "us-east-1b"]
  private_subnets    = ["10.0.1.0/24", "10.0.11.0/24"]
  public_subnets     = ["10.0.101.0/24", "10.0.111.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true
  public_subnet_tags = {
    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/internal-elb"             = 1
  }

}
