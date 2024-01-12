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
            test_variable = "${var.environment_var}"
        }
    }

    tags = {
        project = "d-smart-alpha-site"
        creator = "d_smart"
        resource = "lambda"
    }
}
#Resources end----------------------------------------------------------#
https://aws.amazon.com/getting-started/hands-on/get-a-domain/?ref=gsrchandson&id=updated
https://aws.amazon.com/getting-started/hands-on/get-a-domain/?ref=gsrchandson&id=updated
https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/amplify_app
https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
https://us-east-1.console.aws.amazon.com/route53/v2/hostedzones?region=us-east-1#ListRecordSets/Z058902510ZIZB07I7RKC
https://ap.www.namecheap.com/domains/domaincontrolpanel/d-smart.io/domain
