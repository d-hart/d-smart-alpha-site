#Data start----------------------------------------------------------#
#-----Assume Roles-----#
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    sid    = "basicAssumeRole"
    effect = "Allow"
    # resources = [""]

    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
#-----Assume Roles-----#
#-----Function 1 Role-----#
data "aws_iam_policy_document" "function_1_assume_role_policy" {
  statement {
    sid       = "awsServices"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "ses:*",
      "dynamodb:*",
      "sqs:*",
    ]
  }

  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }
}
#-----Function 1 Role-----#
#-----Function 2 Role-----#
data "aws_iam_policy_document" "function_2_assume_role_policy" {
  statement {
    sid       = "awsServices"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "ses:*",
      "sqs:*",
    ]
  }

  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }
}
#-----Function 2 Role-----#
#-----Function 3 Role-----#
data "aws_iam_policy_document" "function_3_assume_role_policy" {
  statement {
    sid       = "awsServices"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "s3:*",
      "dynamodb:*",
      "sqs:*",
    ]
  }

  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }
}
#-----Function 3 Role-----#
#Data end----------------------------------------------------------#