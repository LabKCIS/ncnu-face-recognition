import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Get the bucket name and the uploaded file name
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    print('Bucket name: {}'.format(bucket_name))
    print('Upload file name: {}'.format(file_name))

    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully!')
    }