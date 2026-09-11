terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "selected" {
  id      = var.vpc_id != "" ? var.vpc_id : null
  default = var.vpc_id == "" ? true : null
}

data "aws_subnets" "selected" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Security group only created when create_ec2 = true, so it costs
# nothing and clutters nothing while the project is dormant.
resource "aws_security_group" "app_sg" {
  count       = var.create_ec2 ? 1 : 0
  name        = "${var.project_name}-sg"
  description = "Allow SSH and API access for ${var.project_name}"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "Flask API"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_instance" "app_server" {
  count                  = var.create_ec2 ? 1 : 0
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id != "" ? var.subnet_id : data.aws_subnets.selected.ids[0]
  vpc_security_group_ids = [aws_security_group.app_sg[0].id]
  key_name               = var.key_pair_name != "" ? var.key_pair_name : null

  tags = {
    Name    = "${var.project_name}-server"
    Project = var.project_name
  }
}
