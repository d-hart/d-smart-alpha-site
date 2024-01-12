import logging
import boto3
import csv
import os
import json
import concurrent.futures
from datetime import datetime, date, timedelta
from botocore.exceptions import ClientError

# set logging level- value options = CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger = logging.getLogger('RptEbsDlmPolicies')
logger.setLevel(logging.DEBUG)

#Variables start------------------------------------------------------------------------------#
email_table = os.environ['email_table']
function_name = os.environ['function_name']
sqs_queue = os.environ['sqs_queue']
resume_bucket = os.environ['resume_bucket']
report = os.environ['report_name']
role_dlm = os.environ['role_dlm']
role_target = os.environ['role_target']
topic = os.environ['topic_arn']
test_variable = os.environ['test_variable']

regions = ['us-east-1']
data = []
output = []
report_list = []

#Variables end------------------------------------------------------------------------------#
def lambda_handler(event, context):
    print(event)
    print(test_variable)
    #Ingest the event information from the front end website
    #Filter out the important information
    #Log the user's information into a DynamoDB table
    #Send the information to the SQS queue
    #Service - DynamoDB, SQS, Cloudwatch