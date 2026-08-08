terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ------------------------------------------------------------------------------
# DynamoDB Tables
# ------------------------------------------------------------------------------

resource "aws_dynamodb_table" "events" {
  name         = "Events"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "eventId"

  attribute {
    name = "eventId"
    type = "S"
  }
}

resource "aws_dynamodb_table" "registrations" {
  name             = "Registrations"
  billing_mode     = "PAY_PER_REQUEST"
  hash_key         = "registrationId"
  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "registrationId"
    type = "S"
  }
}

# ------------------------------------------------------------------------------
# IAM Execution Role & Policies for Lambda
# ------------------------------------------------------------------------------

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_ticketing_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "sns_publish_policy" {
  name = "lambda_sns_publish_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["sns:Publish"]
        Effect   = "Allow"
        Resource = aws_sns_topic.ticket_notifications.arn
      },
      {
        Action = [
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:DescribeStream",
          "dynamodb:ListStreams"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_sns_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.sns_publish_policy.arn
}

# ------------------------------------------------------------------------------
# SNS Notification Topic & Email Subscription
# ------------------------------------------------------------------------------

resource "aws_sns_topic" "ticket_notifications" {
  name = "ticket-confirmations-topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.ticket_notifications.arn
  protocol  = "email"
  endpoint  = "arianaoteng@gmail.com"
}

# ------------------------------------------------------------------------------
# Notification Lambda & Stream Trigger
# ------------------------------------------------------------------------------

resource "aws_lambda_function" "send_notification" {
  filename      = "notification_payload.zip"
  function_name = "sendTicketNotification"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.ticket_notifications.arn
    }
  }
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream_trigger" {
  event_source_arn  = aws_dynamodb_table.registrations.stream_arn
  function_name     = aws_lambda_function.send_notification.arn
  starting_position = "LATEST"
}