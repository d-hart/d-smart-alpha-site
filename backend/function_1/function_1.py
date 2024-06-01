import os
import re
import csv
import json
import boto3
import logging
import concurrent.futures
from botocore.exceptions import ClientError
from datetime import datetime, date, timedelta
# from email_validator import validate_email, EmailNotValidError

# set logging level- value options = CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_table = "d_smart_email_table"
sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/919771552066/d_smart_queue.fifo"

#email_checker end------------------------------------------------------------------------------#
def email_checker(email):
    '''
    Validate the email address the user submitted
    Args:
        email: The email address in string format
    Return:
        valid: Boolean indicating whether the email address is valid
    '''
    regex = r'^[a-z0-9]+[._]?[a-z0-9]+[@]w+[.]w+$'
    try:
        # validate and get info
        print("before email verify")
        if re.match(regex, email):
            print("after email verify")
            # replace with normalized form
            print("True")
            valid = True
        
        else:
            valid = False
            
    except Exception as e:
        print("Email verify failed")
        # email is not valid, exception message is human-readable
        print(str(e))
        valid = False
        
    return valid
#email_checker end------------------------------------------------------------------------------#

#Variables start------------------------------------------------------------------------------#
# email_table = os.environ['email_table']
# function_name = os.environ['function_name']
# sqs_queue = os.environ['sqs_queue']
# resume_bucket = os.environ['resume_bucket']
# report = os.environ['report_name']
# role_dlm = os.environ['role_dlm']
# role_target = os.environ['role_target']
# topic = os.environ['topic_arn']
# test_variable = os.environ['test_variable']

regions = ['us-east-1']
data = []
output = []
report_list = []
#Api request body start------------------------------------------------------------------------------#
# {
    # "price": "400000",
    # "size": "1600",
    # "unit": "sqFt",
    # "downPayment": "20"
# }
#Api request body end------------------------------------------------------------------------------#

#Variables end------------------------------------------------------------------------------#
def lambda_handler(event, context):
    # print(event["body"])
    # print(test_variable)
    dynamodb_client = boto3.client("dynamodb")
    sqs_client = boto3.client("sqs")
    
    print(f"event type: {type(event)}")
    print(f"first name: {event['first_name']}")
    # event_body = json.loads(event['body'])
    # print(type(event_body))
    # print(event_body)
    email = str(event['email'])
    first_name = str(event['first_name'])
    last_name = str(event['last_name'])
    
    valid_email = email_checker(event['email'])
    if email: #valid_email == True:
        try:
            #test this block by giving a valid email address
            db_response = dynamodb_client.put_item(TableName=dynamodb_table,Item={
                'email': {
                    'S': email
                    },
                'first_name': {
                    'S': first_name
                    },
                'last_name': {
                    'S': last_name
                    }
                }
            )
            logger.info("Writing to the database was successful")
            
            body_message = f"Thank you. Your submittion was successful" #, {event['body']}"
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                    },
                "body": body_message
            }
            
            try:
                #test this block by giving a valid email address
                sqs_response = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                MessageBody=event
                            )
            
            except Exception as e:
                #test this block by using the wrong sqs url
                print(f"There was a problem writing to the SQS Queue. Here is the exception \n{e}" )
                body_message = f"Unfortunately. Your submittion failed." #, {event['body']}"
                response = {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                        },
                    "body": body_message
                }
            
        
        except Exception as e:
            #test this block by using the wrong dynamoDB table
            logger.info(f"There was a problem writing to the DynamoDB Table. Here is the exception \n{e}" )
            body_message = f"Unfortunately. Your submittion failed." #, {event['body']}"
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                    },
                "body": body_message
            }

    else: 
        #test this block by giving an invalid email address
        body_message = f"This is not a valid email address. Please try again." #, {event['body']}"
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
                },
            "body": body_message
        }
    
    return response
    
    '''{'resource': '/resume_request', 'path': '/resume_request', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '6167', 'CloudFront-Viewer-Country': 'US', 'Content-Type': 'application/json', 'Host': 'api.d-smart.io', 'Postman-Token': 'df1c4d28-af90-4f3f-99f3-79a9fa1b1bcc', 'Referer': 'http://api.d-smart.io/resume_request', 'User-Agent': 'PostmanRuntime/7.38.0', 'Via': '1.1 8d6071bd169bbf5fd46638140132b1d0.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'guRMsJYO_Z8uqAr9f2t1zQuxyVbHVIlQKifJykG8SUWmqpPHr_SZfw==', 'X-Amzn-Trace-Id': 'Root=1-6654dbff-68f1a45d7c4583920d08b8d5', 'X-Forwarded-For': '174.196.132.134, 130.176.98.77', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['6167'], 'CloudFront-Viewer-Country': ['US'], 'Content-Type': ['application/json'], 'Host': ['api.d-smart.io'], 'Postman-Token': ['df1c4d28-af90-4f3f-99f3-79a9fa1b1bcc'], 'Referer': ['http://api.d-smart.io/resume_request'], 'User-Agent': ['PostmanRuntime/7.38.0'], 'Via': ['1.1 8d6071bd169bbf5fd46638140132b1d0.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['guRMsJYO_Z8uqAr9f2t1zQuxyVbHVIlQKifJykG8SUWmqpPHr_SZfw=='], 'X-Amzn-Trace-Id': ['Root=1-6654dbff-68f1a45d7c4583920d08b8d5'], 'X-Forwarded-For': ['174.196.132.134, 130.176.98.77'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'dpxuc7', 'resourcePath': '/resume_request', 'httpMethod': 'POST', 'extendedRequestId': 'YcdP_ET0IAMEGMQ=', 'requestTime': '27/May/2024:19:16:15 +0000', 'path': '/resume_request', 'accountId': '919771552066', 'protocol': 'HTTP/1.1', 'stage': 'mach-2', 'domainPrefix': 'api', 'requestTimeEpoch': 1716837375634, 'requestId': '29e4080b-a7fa-4ec9-a1b4-48acee548c85', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '174.196.132.134', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.38.0', 'user': None}, 'domainName': 'api.d-smart.io', 'deploymentId': 'sp1zak', 'apiId': 'iowj3ylnkb'}, 'body': '{\n    "first_name": "John ",\n    "last_name": " Doe",\n    "email": "johndoe@hotmail.com",\n    "category": "Cloud Engineering",\n    "role": "contract_role"\n}', 'isBase64Encoded': False}'''
    #Ingest the event information from the front end website
    #Filter out the important information
    #Log the user's information into a DynamoDB table
    #Send the information to the SQS queue to be processed by the second lambda function
    #Service - DynamoDB, SQS, Cloudwatch
    
