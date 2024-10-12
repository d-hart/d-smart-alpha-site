import os
import re
import csv
import json
import boto3
import string
import random
import logging
import concurrent.futures
from botocore.exceptions import ClientError
from datetime import datetime, date, timedelta
# from email_validator import validate_email, EmailNotValidError

# set logging level- value options = CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# dynamodb_table = "d_smart_email_table"


#Variables start------------------------------------------------------------------------------#
sqs_queue = os.environ['sqs_queue']
dynamodb_table = os.environ['email_table']
function_name = os.environ['function_name']
input_variable = os.environ['input_variable']
sqs_queue_url = f"https://sqs.us-east-1.amazonaws.com/{input_variable}/{sqs_queue}.fifo"
# resume_bucket = os.environ['resume_bucket']

regions = ['us-east-1']
data = []
output = []
report_list = []
#Variables end------------------------------------------------------------------------------#

#Api request body start------------------------------------------------------------------------------#
# {
    # "price": "400000",
    # "size": "1600",
    # "unit": "sqFt",
    # "downPayment": "20"
# }
#Api request body end------------------------------------------------------------------------------#

#email_checker end------------------------------------------------------------------------------#
def email_checker(email):
    '''
    Validate the email address the user submitted
    Args:
        email: The email address in string format
    Return:
        valid: Boolean indicating whether the email address is valid
    '''
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    try:
        # validate and get info
        logger.info("before email verify")
        if(re.fullmatch(regex, email)):
            # Email is valid
            logger.info("True")
            valid = True
            logger.info("after email verify is true")
        
        else:
            # Email is not valid
            logger.info("after email verify is false")
            valid = False
            
    except Exception as e:
        logger.info("Email verify failed")
        # email is not valid, exception message is human-readable
        print(str(e))
        valid = False
        
    return valid
#email_checker end------------------------------------------------------------------------------#

def lambda_handler(event, context):
    string_event = str(event)
    print(string_event)
    # updated_string_event = string_event.replace("\'", "\"")
    # event_body = json.loads(updated_string_event)
    
    dynamodb_client = boto3.client("dynamodb")
    sqs_client = boto3.client("sqs")
    customer_dictionary = {}
    # logger.info(f'Event type: {type(event)}')
    # logger.info(f'Event: {event["first_name"]}')
    
    # Define the dictionary to be used later----------------------------------------------------------------------------------------------------------------------------------------#
   
    customer_dictionary["email"] = str(event["email"])
    customer_dictionary["first_name"] = str(event["first_name"])
    customer_dictionary["last_name"] = str(event["last_name"])
    
    valid_email = email_checker(event['email'])
    if valid_email == True: #email:
        # Send the client information to dynamoDB----------------------------------------------------------------------------------------------------------------------------------------#
        try:
            #test this block by giving a valid email address
            db_response = dynamodb_client.put_item(TableName=dynamodb_table,Item={
                'email': {
                    'S': customer_dictionary["email"]
                    },
                'first_name': {
                    'S': customer_dictionary["first_name"]
                    },
                'last_name': {
                    'S': customer_dictionary["last_name"]
                    },
                'contact': {
                    'BOOL':True
                    }
                }
            )
            
            logger.info("Successfully sent the contact information to the dynamoDB table")

            body_message = f"Thank you. Your submittion was successful" #, {event['body']}"
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                    },
                "body": body_message
            }
        
            # Send the payload to SQS for processing----------------------------------------------------------------------------------------------------------------------------------------#
            try:
                #test this block by giving a valid email address
                random_message_group_id = ''.join(random.choices(string.ascii_letters,k=7))
                sqs_response = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                MessageBody=str(event),
                                MessageGroupId = random_message_group_id
                            )
                logger.info("Successfully sent the event to the sqs queue")
            
            except Exception as e:
                #test this block by using the wrong sqs url
                logger.info(f"Failed to send the event to the SQS Queue. Here is the exception \n{e}" )
                
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
            logger.info(f"Failed to send the contact information to the DynamoDB Table. Here is the exception \n{e}" )
            
            body_message = f"Unfortunately. Your information failed to reach its destination." #, {event['body']}"
            response = {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                    },
                "body": body_message
            }

    else: 
        #test this block by giving an invalid email address
        logger.info("The email address provided was invalid. Gracefully exit the program")
       
        body_message = f"This is not a valid email address. Please try again." #, {event['body']}"
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
                },
            "body": body_message
        }
    
    return response
    
    #Ingest the event information from the front end website
    #Filter out the important information
    #Log the user's information into a DynamoDB table
    #Send the information to the SQS queue to be processed by the second lambda function
    #Service - DynamoDB, SQS, Cloudwatch
    
