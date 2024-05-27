#Resources start----------------------------------------------------------#
resource "aws_amplify_app" "d_smart_app" {
  name                        = var.app_name
  repository                  = var.repository
  oauth_token                 = var.token
  enable_auto_branch_creation = true

  # The default patterns added by the Amplify Console.
  auto_branch_creation_patterns = [
    "*",
    "*/**",
  ]
  auto_branch_creation_config {
    # Enable auto build for the created branch.
    enable_auto_build = true
  }
}

resource "aws_amplify_branch" "amplify_branch" {
  app_id      = aws_amplify_app.d_smart_app.id
  branch_name = var.branch_name
}

resource "aws_amplify_domain_association" "domain_association" {
  app_id                = aws_amplify_app.d_smart_app.id
  domain_name           = var.domain_name
  wait_for_verification = false

  sub_domain {
    branch_name = aws_amplify_branch.amplify_branch.branch_name
    prefix      = var.branch_name
  }
  # https://d-smart.io
  sub_domain {
    branch_name = aws_amplify_branch.amplify_branch.branch_name
    prefix      = ""
  }

  # https://www.d-smart.io
  sub_domain {
    branch_name = aws_amplify_branch.amplify_branch.branch_name
    prefix      = "www"
  }
}

#Resources end----------------------------------------------------------#