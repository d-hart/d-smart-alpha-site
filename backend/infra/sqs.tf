resource "aws_sqs_queue" "d_smart_queue" {
  name                        = "${var.d_smart_queue}.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  visibility_timeout_seconds  = 1000
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_sqs_queue.d_smart_queue.arn
  enabled          = true
  function_name    = var.function_2
  batch_size       = 1
}