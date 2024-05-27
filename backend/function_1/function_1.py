import os
import csv
import json
import time
import boto3
import pprint
import logging
import concurrent.futures
from datetime import datetime, date, timedelta
from botocore.exceptions import ClientError

# set logging level- value options = CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger = logging.getLogger('RptEbsDlmPolicies')
logger.setLevel(logging.DEBUG)

#Variables start------------------------------------------------------------------------------#
# sqs_queue = os.environ['sqs_queue']
# email_table = os.environ['email_table']
# function_name = os.environ['function_name']
# resume_bucket = os.environ['resume_bucket']

regions = ['us-east-1']
data = []
output = []
report_list = []
#Api request body start------------------------------------------------------------------------------#
event_sample = {'resource': '/resume_request', 'path': '/resume_request', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '7922', 'CloudFront-Viewer-Country': 'US', 'Content-Type': 'application/json', 'Host': 'api.d-smart.io', 'Postman-Token': '6c0ce9c5-3184-4703-927b-9b83fa6fb1e9', 'Referer': 'http://api.d-smart.io/resume_request', 'User-Agent': 'PostmanRuntime/7.36.3', 'Via': '1.1 9c90b41a9e5ac2856624d29ed4da4234.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': '4nWeSV2kFNoZH64XIMRAItIVRK9zJR21zGJ_33tHl8Afq9sWhGAdzQ==', 'X-Amzn-Trace-Id': 'Root=1-65ec9e2b-5f929e9b0bda08a817adfcba', 'X-Forwarded-For': '69.255.165.98, 130.176.98.151', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['7922'], 'CloudFront-Viewer-Country': ['US'], 'Content-Type': ['application/json'], 'Host': ['api.d-smart.io'], 'Postman-Token': ['6c0ce9c5-3184-4703-927b-9b83fa6fb1e9'], 'Referer': ['http://api.d-smart.io/resume_request'], 'User-Agent': ['PostmanRuntime/7.36.3'], 'Via': ['1.1 9c90b41a9e5ac2856624d29ed4da4234.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['4nWeSV2kFNoZH64XIMRAItIVRK9zJR21zGJ_33tHl8Afq9sWhGAdzQ=='], 'X-Amzn-Trace-Id': ['Root=1-65ec9e2b-5f929e9b0bda08a817adfcba'], 'X-Forwarded-For': ['69.255.165.98, 130.176.98.151'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'dpxuc7', 'resourcePath': '/resume_request', 'httpMethod': 'POST', 'extendedRequestId': 'UX2m4EuToAMEYUA=', 'requestTime': '09/Mar/2024:17:36:43 +0000', 'path': '/resume_request', 'accountId': '919771552066', 'protocol': 'HTTP/1.1', 'stage': 'mach-2', 'domainPrefix': 'api', 'requestTimeEpoch': 1710005803769, 'requestId': 'f8339eee-a8fa-4f39-8015-b0d41c11a2ce', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '69.255.165.98', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.36.3', 'user': None}, 'domainName': 'api.d-smart.io', 'deploymentId': 'sp1zak', 'apiId': 'iowj3ylnkb'}, 'body': '{\n    "first_name": "John ",\n    "last_name": " Doe",\n    "email": "johndoe@hotmail.com",\n    "category": "Cloud Engineering",\n    "role": "contract_role"\n}', 'isBase64Encoded': False}
#Api request body end------------------------------------------------------------------------------#




#Variables end------------------------------------------------------------------------------#
def lambda_handler(event_sample): #, context
    event_data = json.loads(event_sample['body'])
    pprint.pprint(event_data)
    # print(test_variable)
    
    email_table = "email_table"
    sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/919771552066/d_smart_queue.fifo"
    
    first_name = event_data['first_name'].replace(" ", "")
    last_name = event_data['last_name'].replace(" ", "")
    email = event_data['email'].replace(" ", "")
    # print(first_name)
    # my_session = boto3.session.Session()
    # dynamodb_client = my_session.client("dynamodb")

    dynamodb_client = boto3.client('dynamodb')
    response = dynamodb_client.put_item(TableName=email_table,
                                        Item={
                                           'Email':{
                                               'S':email
                                           },
                                           'first_name':{
                                               'S':first_name
                                           },
                                           'last_name':{
                                               'S':last_name
                                           }
                                        }
                                    )
    
    sqs_client = boto3.client('sqs')
    response = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                MessageBody=event_data['body'],
                                MessageGroupId="time.time()"
                            )
    
    
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": "Connection to Lambda was successful!"
    }
    
    return response

if __name__ == "__main__":
    lambda_response = lambda_handler(event_sample)


    #Ingest the event information from the front end website
    #Filter out the important information
    #Log the user's information into a DynamoDB table
    #Send the information to the SQS queue to be processed by the second lambda function
    #Service - DynamoDB, SQS, Cloudwatch

