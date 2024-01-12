variable "token" {
  type = string
  description = "github token to connect github repo"
  default = ""
}

variable "repository" {
  type = string
  description = "github repo url"
  default = "https://github.com/d-hart/d-smart-alpha-site"
}

variable "app_name" {
  type = string
  description = "AWS Amplify App Name"
  default = "D_smart_App"
}

variable "branch_name" {
  type = string
  description = "AWS Amplify App Repo Branch Name"
  default = "main"
}

variable "domain_name" {
  type = string
  description = "AWS Amplify Domain Name"
  default = "d-smart.io"
}