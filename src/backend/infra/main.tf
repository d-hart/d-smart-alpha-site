#Providers start----------------------------------------------------------#
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.30.0"
    }
  }
  
  required_version = ">=1.6.0"

  backend "s3" {
    bucket = "djh-terraform-course"

    key = "alpha_site.tfstate"

    region = "us-east-1"

    profile = "spike"

    dynamodb_table = "cloudcast-terraform-course"
  }
}

provider "aws" {
  region  = var.default_region
  profile = "spike"
}
#Providers end----------------------------------------------------------#