# resource "aws_ses_email_identity" "email_sender" {
#   email = var.email_sender
# }

resource "aws_ses_domain_identity" "d_smart" {
  domain = var.domain_name
}

resource "aws_route53_record" "ses_verification" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = "amazonses.email"
  type    = "TXT"
  records = [aws_ses_domain_identity.d_smart.verification_token]
  ttl     = "600"
}

resource "aws_ses_configuration_set" "d_smart" {
  name = "d_smart_configuration_set"
  reputation_metrics_enabled = true
}

output "ses_configuration_set_name" {
  value = aws_ses_configuration_set.d_smart.name
}