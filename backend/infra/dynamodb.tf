#Resources start----------------------------------------------------------#
resource "aws_dynamodb_table" "email_table" {
  name           = "email_table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "Email"


  attribute {
    name = "Email"
    type = "S"
  }

  #    lifecycle {
  #     prevent_destroy = true
  #   }

  tags = {
    project  = "d-smart-alpha-site"
    creator  = "d_smart"
    resource = "dynamodb"
  }
}
#Resources end----------------------------------------------------------#