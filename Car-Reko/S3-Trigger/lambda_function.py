import json

import base64

import boto3

from datetime import datetime

from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key

import os
 
import time

demo_table = resource('dynamodb').Table('car_parking')


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Get the bucket name and the uploaded file name
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']

    print('Bucket name: {}'.format(bucket_name))
    print('Upload file name: {}'.format(file_name))
    #get current unix time
    created = int(datetime.now().timestamp())
    #OCR
    textRekoResult = ocr(bucket_name,file_name)
    data = {}
    data['car_no'] = textRekoResult
    dateResponse = data
    data['upload_file_name'] = file_name
    data['created'] = created
    print(json.dumps(data))
    #dateResponse = data
    #Write DynamoDB
    insertDB(created,textRekoResult,file_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully!')
    }

def ocr(Bucket,key):
    client=boto3.client('rekognition')
    response=client.detect_text(Image={'S3Object':{'Bucket':Bucket,'Name':key}})
    detectedText = response['TextDetections']
    print("Congratulations! You just fetched text from the image successfully. Total number of responses fetched from the given image {}".format(len(detectedText)))
    #Iterate through detectedText to get the required name/value pairs. 
    result = ''
    for text in detectedText:
        #Get DetectedText
        print('Detected Text:' + text['DetectedText'], end=" ")
        result = text['DetectedText']
        #Get the Confidence 
        print('Confidence:' + "{}".format(round(text['Confidence'])) + '%', end=" ")
        #Get the type of the text
        print('Text Type:' + text['Type'])
        print("-")
    return  result

def insertDB(created,car_no,fileName):
    print(f'demo_insert')
    response = demo_table.put_item(
        Item={
                'created': created, # parition key
                'car_no' : car_no,  # sort key
                'enter_image': fileName,
                'exit_image' : "None",
                'exit_time':0,
                'status':'enter'
            }
        )
    print(f'Insert response: {response}')