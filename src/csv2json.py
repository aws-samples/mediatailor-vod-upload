import json
import csv
import boto3
from itertools import islice

maxvod = 1000 # limit import rows per https://docs.aws.amazon.com/mediatailor/latest/ug/quotas.html

s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get the object from the event 
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    data = []
   
    try:
        #load CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf-8').split('\n')
    
        #loop convert each row of CSV to JSON
        for row in islice(csv.DictReader(lines),maxvod):
            data.append(row)  
        return json.loads(json.dumps(data, indent=2))

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e