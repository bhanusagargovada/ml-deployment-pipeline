output "instance_public_ip" {
  description = "Public IP of the EC2 instance (empty when create_ec2 = false)"
  value       = var.create_ec2 ? aws_instance.app_server[0].public_ip : null
}

output "instance_id" {
  description = "EC2 instance ID (empty when create_ec2 = false)"
  value       = var.create_ec2 ? aws_instance.app_server[0].id : null
}

output "api_url" {
  description = "URL to reach the deployed Flask API (empty when create_ec2 = false)"
  value       = var.create_ec2 ? "http://${aws_instance.app_server[0].public_ip}:5000" : null
}
