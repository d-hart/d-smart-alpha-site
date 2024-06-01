#Variables start----------------------------------------------------------#
variable "default_region" {
  type    = string
  default = "us-east-1"
}

variable "function_1" {
  type    = string
  default = "function_1"
}

variable "function_2" {
  type    = string
  default = "function_2"
}

variable "function_3" {
  type    = string
  default = "function_3"
}

# variable "email_table" {
# type = string
# default = aws_dynamodb_table.email_table.name
# }

variable "token" {
  type        = string
  description = "github token to connect github repo"
  default     = ""
}

variable "repository" {
  type        = string
  description = "github repo url"
  default     = "https://github.com/d-hart/d-smart-alpha-site"
}

variable "app_name" {
  type        = string
  description = "AWS Amplify App Name"
  default     = "D_Smart_App"
}

variable "branch_name" {
  type        = string
  description = "AWS Amplify App Repo Branch Name"
  default     = "main"
}

variable "domain_name" {
  type        = string
  description = "AWS Amplify Domain Name"
  default     = "d-smart.io"
}
# https://d-smart.io
variable "stage_name" {
  type        = string
  description = "The name of the stage"
  default     = "mach-2"
}

variable "path_part" {
  type        = string
  description = "The name of the path_part"
  default     = "resume_request"
}

variable "d_smart_queue" {
  type        = string
  description = "The name of the sqs queue"
  default     = "d_smart_queue"
}

variable "input_variable" {
  type    = string
  default = "919771552066"
}

variable "email_table" {
  type        = string
  description = "The name of the dynamodb table"
  default     = "d_smart_email_table"
}

# var.email_sender
variable "email_sender" {
  type        = string
  description = "The name of the email address"
  default     = "noreply@d-smart.io"
}

variable "d_smart_s3_bucket" {
  type        = string
  description = "The name of the s3 bucket"
  default     = "d_smart_s3_bucket"
}
#Variables end----------------------------------------------------------#