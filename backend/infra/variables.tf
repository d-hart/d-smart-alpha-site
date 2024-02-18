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
  default     = "https://github.com/d-hart/d-smart-alpha-site.git"
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
#Variables end----------------------------------------------------------#