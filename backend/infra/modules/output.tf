#Output start----------------------------------------------------------#
output "lambda_arn" {
    value = aws_lambda_function.lambda_function.arn
}

output "lambda_name" {
    value = aws_lambda_function.lambda_function.function_name
}

output "lambda_invoke_arn" {
    value = aws_lambda_function.lambda_function.invoke_arn
}
#Output end----------------------------------------------------------#