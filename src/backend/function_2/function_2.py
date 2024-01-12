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

regions = ['us-east-1']
data = []
output = []
report_list = []

#Variables end------------------------------------------------------------------------------#
def lambda_handler(event, context):
    print(event)
    #Recieve the information from the sqs queue
    #Filter out the email and first name from the first function
    #Format the information to be sent to SES
    #Send the information to SES
    #Service - SQS, SES, Cloudwatch