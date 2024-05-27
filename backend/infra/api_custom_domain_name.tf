resource "aws_api_gateway_domain_name" "api" {
  domain_name     = "api.${var.domain_name}"
  certificate_arn = aws_acm_certificate_validation.api.certificate_arn
  security_policy = "TLS_1_2"
  endpoint_configuration {
    types = ["EDGE"]
  }
  depends_on = [aws_acm_certificate_validation.api]
}

resource "aws_route53_record" "api" {
  name    = "api.${var.domain_name}"
  type    = "A"
  zone_id = data.aws_route53_zone.public.zone_id

  alias {
    name                   = aws_api_gateway_domain_name.api.cloudfront_domain_name
    zone_id                = aws_api_gateway_domain_name.api.cloudfront_zone_id
    evaluate_target_health = true
  }

  depends_on = [aws_acm_certificate_validation.api]
}

# aws_api_gateway_domain_name.api.cloudfront_zone_id
# aws apigateway get-domain-names

# resource "aws_apigatewayv2_domain_name" "api" {
#   domain_name = "api.${var.domain_name}"

#   domain_name_configuration {
#     certificate_arn = aws_acm_certificate.api.arn
#     endpoint_type   = "REGIONAL"
#     security_policy = "TLS_1_2"
#   }

#   depends_on = [aws_acm_certificate_validation.api]
# }