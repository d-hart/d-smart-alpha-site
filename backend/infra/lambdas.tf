#Modules start----------------------------------------------------------#
module "function_1" {
  source        = "./modules"
  function_name = var.function_1
  code_source   = "../${var.function_1}"
  handler       = "function_1.lambda_handler"
  assume_role   = aws_iam_role.lambda_exec_role_1.arn
  environment_vars = {
    function_name  = "${var.function_1}"
    email_table    = "${var.email_table}" # aws_dynamodb_table.email_table.id
    sqs_queue      = "${var.d_smart_queue}"
    input_variable = "${var.input_variable}"
  }
}
module "function_2" {
  source        = "./modules"
  function_name = var.function_2
  code_source   = "../${var.function_2}"
  handler       = "function_2.lambda_handler"
  assume_role   = aws_iam_role.lambda_exec_role_2.arn
  environment_vars = {
    function_name = "${var.function_1}"
    email_table   = "${var.email_table}" # aws_dynamodb_table.email_table.id
    sqs_queue     = "${var.d_smart_queue}"
  }
}

module "function_3" {
  source        = "./modules"
  function_name = var.function_3
  code_source   = "../${var.function_3}"
  handler       = "function_3.lambda_handler"
  assume_role   = aws_iam_role.lambda_exec_role_3.arn
  environment_vars = {
    test_variable = "function_3_test_variable"
    s3_bucket     = "${var.d_smart_s3_bucket}"
  }
  #   function_name = os.environ['function_name']
  #   sqs_queue = os.environ['sqs_queue']
  #   resume_bucket = os.environ['resume_bucket']
  #   report = os.environ['report_name']
  #   role_dlm = os.environ['role_dlm']
  #   role_target = os.environ['role_target']
  #   topic = os.environ['topic_arn']
  #   test_variable = os.environ['test_variable']
}
#Modules end----------------------------------------------------------#

#Resources start----------------------------------------------------------#
#-----Lambda 1 Execution Roles-----#
resource "aws_iam_role" "lambda_exec_role_1" {
  name               = "serverless_lambda1"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_policy" "function_1_policy" {
  name        = "function_1_policy"
  description = "The policy created for the first lambda function"
  policy      = data.aws_iam_policy_document.function_1_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "policy_attach_1" {
  role       = aws_iam_role.lambda_exec_role_1.name
  policy_arn = aws_iam_policy.function_1_policy.arn
}
#-----Lambda 1 Execution Roles-----#

#-----Lambda 2 Execution Roles-----#
resource "aws_iam_role" "lambda_exec_role_2" {
  name               = "serverless_lambda2"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_policy" "function_2_policy" {
  name        = "function_2_policy"
  description = "The policy created for the second lambda function"
  policy      = data.aws_iam_policy_document.function_2_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "policy_attach_2" {
  role       = aws_iam_role.lambda_exec_role_2.name
  policy_arn = aws_iam_policy.function_2_policy.arn
}
#-----Lambda 2 Execution Roles-----#

#-----Lambda 3 Execution Roles-----#
resource "aws_iam_role" "lambda_exec_role_3" {
  name               = "serverless_lambda3"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_policy" "function_3_policy" {
  name        = "function_3_policy"
  description = "The policy created for the third lambda function"
  policy      = data.aws_iam_policy_document.function_3_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "policy_attach_3" {
  role       = aws_iam_role.lambda_exec_role_3.name
  policy_arn = aws_iam_policy.function_3_policy.arn
}
#-----Lambda 3 Execution Roles-----#
#Resources end----------------------------------------------------------#
