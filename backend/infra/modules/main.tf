#Data start----------------------------------------------------------#
data "archive_file" "name" {
    type = "zip"
    source_dir = var.code_source
    output_path = "${var.function_name}.zip"
}
#Data end----------------------------------------------------------#
#Locals start----------------------------------------------------------#
locals {
  environment_map = var.environment_vars[*]
}
#Locals end----------------------------------------------------------#
#Resources start----------------------------------------------------------#
resource "aws_lambda_function" "lambda_function" {
    function_name = var.function_name
    filename = "${var.function_name}.zip"
    description = "The lambda function is designed to provide a self service resume portal"
    memory_size = 3000
    timeout = 900
    handler = var.handler
    runtime = "python3.9"
    role = var.assume_role
    layers = var.layers

    dynamic "environment" {
        for_each = local.environment_map
        content {
          variables = environment.value
        }
      }

    tags = {
        project = "d-smart-alpha-site"
        creator = "d_smart"
        resource = "lambda"
    }
}
#Resources end----------------------------------------------------------#