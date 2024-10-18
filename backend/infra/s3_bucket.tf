resource "aws_s3_bucket" "d_smart_s3_bucket" {
  bucket = var.d_smart_s3_bucket

  tags = {
    Name    = var.d_smart_s3_bucket
    Project = "d-smart-alpha-site"
  }
}