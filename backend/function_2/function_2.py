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
logger.setLevel(logging.DEBUG)
domain_email_address = 'no-reply@d-smart.io'
test_receive_email_address = 'durellhart@live.com'

# AWS CLI S3 command to upload the Resume
# aws s3 cp ~/Documents/Professional/Durell_Hart_Resume_October_2024.pdf s3://d-smart-s3-bucket/Durell_Hart_Resume_Current.pdf

#Variables start----------------------------------------------------------------------------------------------------------------------------------------#
# function_name = os.environ['function_name']
resume_bucket = "d-smart-s3-bucket" #os.environ['resume_bucket']

regions = ['us-east-1']
data = []
output = []
report_list = []

#Variables end----------------------------------------------------------------------------------------------------------------------------------------#
def lambda_handler(event, context):
    # Build the necessary clients
    ses_clients = boto3.client('ses')
    s3_client = boto3.client('s3')
    
    # Filter out the email and first name from the first function & SQS Queue----------------------------------------------------------------------------------------------------------------------------------------#
    for element in event['Records']:
        customer_dictionary = {}
        element_body_object = element['body'].replace("\'", "\"")
        event_json_object = json.loads(element_body_object)
        print(type(event_json_object))
        print(event_json_object)
        
        customer_dictionary["email"] = str(event_json_object["email"])
        customer_dictionary["first_name"] = str(event_json_object["first_name"])
        customer_dictionary["last_name"] = str(event_json_object["last_name"])
    
    #Reach out to AWS S3 bucket to get a link to the resume document----------------------------------------------------------------------------------------------------------------------------------------#
    print(f'First Name: {event_json_object["first_name"]}')
    
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
        ExpiresIn=3600,
        HttpMethod=None
    )
    
    #Format the information to be sent to SES with the S3 link----------------------------------------------------------------------------------------------------------------------------------------#
    html = """\
    <html>
      <head></head>
      <body>
        <p>Greetings """ +str(customer_dictionary["first_name"])+""",<br>
        <br>
        Per your request, here is a <a href='"""+str(url)+"""'>link</a> to my current resume. Access to this link will expire in 1 hour. Thank you for visiting my web application/website. Please let me know if you have any questions and take care of yourself.<br>
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
                    test_receive_email_address, #customer_dictionary["email"] # muzzle mode
                ]
            },
            Message=message
        )
        print(f"You successfully sent the email to {test_receive_email_address}") # muzzle mode
        
    except Exception as e:
                # test this block by sending an invalid email
                logger.info(f"Failed to send the email to {test_receive_email_address}. Here is the exception \n{e}" ) # muzzle mode
                
    print('Program end.')

# Local machine runs only----------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    event_api = {
        'Records': 
        [
            {
                'messageId': 'couixz348792-4ccd-9021-90d3-3849038420234', 
                'receiptHandle': 'stuff_on_this_line', 
                'body': '{"first_name": "John", "last_name": "Doe", "email": "johndoe@email.com"}',
                'attributes': {
                    'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-67dsgsdgfd95901sdgfdsgc176e;Parent=1a34kj5h3k5h433;Sampled=0;Lineage=1:0345435c9:0', 
                    'SentTimestamp': '1728512971266', 'SequenceNumber': '188892433df94353647616', 'MessageGroupId': 'Jfdfd8984', 'SenderId': 'gdfgdsfgsdfggsgdf:function_1', 
                    'MessageDeduplicationId': '31c51d3307efcbfdsgfgsdfsgsdfgs54461977104e68b0b638932c8', 
                    'ApproximateFirstReceiveTimemp': 'lskdfjsdlkfjl323498274'
                }, 
                'messageAttributes': {}, 
                'md5OfBody': 'jkadhfs89732948jsdbfkj298347kjhdsk', 
                'eventSource': 'aws:sqs', 
                'eventSourceARN': 'arn:aws:sqs:us-east-1:319760898065:d_smart_queue.fifo', 
                'awsRegion': 'us-east-1'
            }
        ]
    }
    context = ''
    lambda_handler(event_api,context)
# Local machine runs only----------------------------------------------------------------------------------------------------------------------------------------#   
    