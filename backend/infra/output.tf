output "endpoint_url" {
  value = "${aws_api_gateway_stage.api_stage.invoke_url}/${var.path_part}"
}