variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix for resources"
  type        = string
  default     = "ml-deployment-pipeline"
}

variable "create_ec2" {
  description = "Whether to actually create the EC2 instance. Keep false to avoid any cost; set true only when demoing."
  type        = bool
  default     = false
}

variable "instance_type" {
  description = "EC2 instance type (t2.micro / t3.micro are free-tier eligible)"
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "Existing EC2 key pair name for SSH access"
  type        = string
  default     = ""
}

variable "vpc_id" {
  description = "VPC ID to launch the instance in. Leave empty to use the default VPC."
  type        = string
  default     = ""
}

variable "subnet_id" {
  description = "Subnet ID to launch the instance in. Leave empty to use the default subnet."
  type        = string
  default     = ""
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to SSH into the instance"
  type        = string
  default     = "0.0.0.0/0"
}
