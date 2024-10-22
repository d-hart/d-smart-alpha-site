resource "aws_api_gateway_base_path_mapping" "api" {
  api_id      = aws_api_gateway_rest_api.api.id
  stage_name  = var.stage_name
  domain_name = aws_api_gateway_domain_name.api.domain_name
  # base_path   = "/" #var.path_part #${aws_api_gateway_deployment.deployment.stage_name}/
  depends_on = [aws_api_gateway_stage.api_stage]
}

# output "cloudfront_domain_name" {
#   value = "https://${aws_api_gateway_domain_name.api.cloudfront_domain_name}"
# }

output "aws_api_gateway_stage_name" {
  value = var.stage_name
}