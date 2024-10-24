import logging
import boto3
import csv
import os
import json
import concurrent.futures
from datetime import datetime, date, timedelta
from botocore.exceptions import ClientError

# set logging level- value options = CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
logger = logging.getLogger()
logger.setLevel(logging.INFO)
domain_email_address = 'no-reply@d-smart.io'
test_receive_email_address = 'durellhart@live.com'

# AWS CLI S3 command to upload the Resume
# aws s3 cp ~/Documents/Professional/Durell_Hart_Resume_October_2024.pdf s3://d-smart-s3-bucket/Durell_Hart_Resume_Current.pdf

#Variables start----------------------------------------------------------------------------------------------------------------------------------------#
function_name = os.environ['function_name']
resume_bucket = "d-smart-s3-bucket" #os.environ['resume_bucket']

regions = ['us-east-1']
data = []
output = []
report_list = []

# Variables end----------------------------------------------------------------------------------------------------------------------------------------#
def lambda_handler(event, context):
    # Build the necessary clients
    ses_clients = boto3.client('ses')
    s3_client = boto3.client('s3')
    
    # Filter out the email and first name from the first function & SQS Queue----------------------------------------------------------------------------------------------------------------------------------------#
    # print(f"event: {event['Records']}")

    for element in event['Records']:
        print(f"element body: {element['body']}")
        print(f"element body type: {type(element['body'])}")
        customer_dictionary = {}
        # element_body_object = element['body'].replace("\'", "\"")
        json_dict_event_body = json.loads(element['body'])
        print(f"json_dict_event_body: {json_dict_event_body}")
        print(f"json_dict_event_body type: {type(json_dict_event_body)}")
        
        customer_dictionary["email"] = str(json_dict_event_body["email"])
        customer_dictionary["first_name"] = str(json_dict_event_body["first_name"])
        customer_dictionary["last_name"] = str(json_dict_event_body["last_name"])
    
    # print(f"customer_dictionary: {customer_dictionary}")
    # print(f'First Name: {json_dict_event_body["first_name"]}')
    # Reach out to AWS S3 bucket to get a link to the resume document----------------------------------------------------------------------------------------------------------------------------------------#
    
    bucket_objects = s3_client.list_objects(
        Bucket=resume_bucket)
    
    for resume in bucket_objects['Contents']:#['ResponseMetadata']:
        print(resume['Key'])
        resume_name = resume['Key']
    
    # Generate the presigned URL to the resume document----------------------------------------------------------------------------------------------------------------------------------------#
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': resume_bucket,
            'Key': resume_name
        },
        ExpiresIn=86400,
        HttpMethod=None
    )
    print(f"S3 url: {url}")
    
    # Format the information to be sent to SES with the S3 link----------------------------------------------------------------------------------------------------------------------------------------#
    html = """\
    <html>
      <head></head>
      <body>
        <p>Greetings """ +str(customer_dictionary["first_name"])+""",<br>
        <br>
        Per your request, here is a <a href='"""+str(url)+"""'>link</a> to my current resume. Access to this link will expire in 24 hours. Thank you for visiting my web application/website. Please let me know if you have any questions and take care of yourself.<br>
        <br>
        Sincerely,<br>
        <br>
        Durell J. Hart<br>
        </p>
      </body>
    </html>
    """
    print(url)
    
    subject = "Durell Hart's Resume"
    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": html}}}
    
    # Send the information to SES----------------------------------------------------------------------------------------------------------------------------------------#
    try:
        
        resonse = ses_clients.send_email(
            Source=domain_email_address,
            Destination={
                'ToAddresses': [
                    customer_dictionary["email"], # muzzle mode replace with test_receive_email_address
                ]
            },
            Message=message
        )
        print(f'You successfully sent the email to {customer_dictionary["email"]}') # muzzle mode replace with test_receive_email_address
        
    except Exception as e:
                # test this block by sending an invalid email
                logger.info(f'Failed to send the email to {customer_dictionary["email"]}. Here is the exception \n{e}' ) # muzzle mode replace with test_receive_email_address
                
    print('Program end.')

# Local machine runs only----------------------------------------------------------------------------------------------------------------------------------------#
# if __name__ == "__main__":
# event: {
#     'Records': [
#         {
#             'messageId': '23c783dd-f4c50a', 
#             'receiptHandle': 'AQqwredfsEBdq', 
#             'body': '{"first_name": "John", "last_name": "Doe", "email": "johndoe@testemail.com", "category": "python_aws_cloud_development", "role_type": "full_time", "human_checkbox": true, "message": "My company loves you and I would like to have a copy of your resume."}', 
#             'attributes': 
#             {
#                 'ApproximateReceiveCount': '1', 
#                 'AWSTraceHeader': 'ewr4dssdfdc9:0', 
#                 'SentTimestamp': '172945564', 
#                 'SequenceNumber': 'dsffds', 
#                 'MessageGroupId': 'RwixwKQ', 
#                 'SenderId': 'fds2:function_1', 
#                 'MessageDeduplicationId': 'sdffdsfsads', 
#                 'ApproximateFirstReceiveTimestamp': 'wtre3452'
#             }, 
#             'messageAttributes': {}, 
#             'md5OfBody': 'upiqeohajkls', 
#             'eventSource': 'aws:sqs', 
#             'eventSourceARN': 'arn:aws:sqs:us-west-2:2345:queue.', 
#             'awsRegion': 'us-east-2'
#         }
#     ]
# }
#     context = ''
#     lambda_handler(event_api,context)
# Local machine runs only----------------------------------------------------------------------------------------------------------------------------------------#   
    