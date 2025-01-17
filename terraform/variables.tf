variable "additional_tags" {
  description = "Additional resource tags"
  type        = map(string)
  default = {
    terraform = "true"
  }
}

variable "aws_region" {
  description = "Region in which the resources are provisioned"
  type        = string
  default     = "us-east-2"
}

variable "api_name" {
  description = "Name appended to resources specific to the infrastructure of the api"
  type        = string
  default     = "api"
}

variable "enable_nat_gateway" {
  description = "Should be true if you want your Fargate tasks to access the public internet"
  type        = bool
  default     = "false"
}
variable "fargate_memory" {
  description = "Amount of memory allocated for the ECS task"
  type        = number
  default     = 512
}

variable "fargate_memory_reserved" {
  description = "Amount of memory reserved for the ECS task"
  type        = number
  default     = 256
}

variable "fargate_cpu" {
  description = "Amount of cpu allocated for the ECS Fargate task"
  type        = number
  default     = 256
}
