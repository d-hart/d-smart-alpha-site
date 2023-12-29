#Data start----------------------------------------------------------#
data "archive_file" "name" {
    type = "zip"
    source_dir = var.code_source
    output_path = "${var.function_name}.zip"
}
#Data end----------------------------------------------------------#
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

    environment {
        variables = {
            test_variable = "${var.enviroment_var}"
        }
    }

    tags = {
        project = "alpha_site"
        creator = "d_smart"
        resource = "lambda"
    }
}
#Resources end----------------------------------------------------------#