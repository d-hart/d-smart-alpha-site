#Resources start----------------------------------------------------------#
resource "aws_dynamodb_table" "email_table" {
  name           = "${var.email_table}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "email"


  attribute {
    name = "email"
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