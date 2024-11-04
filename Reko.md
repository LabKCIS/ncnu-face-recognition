---
# Course Material
---
# AWS Rekognition(車牌辨識) With Line Notify 實作
## 架構圖


*使用AWS S3,Lambda,Rekognition,DynamoDB等服務,並把上傳到S3的圖檔做車牌辨識,結果透過Line Notify通知*

![image](https://hackmd.io/_uploads/Hy__UGT7p.png)

# 先前準備
## 建立S3 Bucket 並增加兩個目錄
Block all public access設定取消,並點選Turning off block all public access

![image](https://hackmd.io/_uploads/rkgyXbTXp.png)

![image](https://hackmd.io/_uploads/H15Xfx6Qa.png)

| Name | Desc |
| ---- | ---- |
| car_image     |   上傳辨識圖檔   |
|     QRCode |  存放產生的QRcode    |
## 設定S3 Bucket Bucket policy
![image](https://hackmd.io/_uploads/r1CG-Zp7T.png)
設定此Bucket的每一個Object都可以公開讀取
設定值範例如下
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Stmt1405592139000",
			"Effect": "Allow",
			"Principal": "*",
			"Action": "s3:GetObject",
			"Resource": [
				"arn:aws:s3:::xxxxx/*",
				"arn:aws:s3:::xxxxx"
			]
		}
	]
}
```

*其中xxxxx請改為新建立的Bucket Name*



## 申請LineNotify 權杖
1.先登入Line開發者帳號
https://notify-bot.line.me/my/

2.選擇行動條碼登入
![image](https://hackmd.io/_uploads/rJ5KQgTQT.png)

3.透過Line掃描行動條碼
![image](https://hackmd.io/_uploads/ByiqVlaQp.png)

4.確定登入
![image](https://hackmd.io/_uploads/rJ7CBeaQp.png)

5.選擇發行權杖
![image](https://hackmd.io/_uploads/HJBLrgaQa.png)

6.輸入Notify名稱及選擇要通知的群組
![image](https://hackmd.io/_uploads/HJjiBx6Q6.png)
最後按發行

7.複製產生的權杖
![image](https://hackmd.io/_uploads/r1_yPlTQ6.png)

8.Line Notify通知已發行權杖
![image](https://hackmd.io/_uploads/rkspPgamT.png)

## Dynamo DB 新增一個Table
![image](https://hackmd.io/_uploads/ryDrw-676.png)
1.按Create Table
![image](https://hackmd.io/_uploads/HJfFPbp7p.png)
2.相關設定如下
![image](https://hackmd.io/_uploads/BJb1FbTQ6.png)


*Table Name: car_parking*




欄位設定

| Name    | Type   | Note        |
| ------- | ------ | ----------- |
| created | Number | Partion Key |
| car_no        | String       |Sort Key              |


## 新增Lambda Layer儲存的S3 Bucket
1.新增S3 Bucket

2.下載lambda layer

下載網址如下

https://github.com/LabKCIS/ncnu-face-recognition/blob/main/QRCode-Layer/lambda-layer-qrcode.zip

3.上傳QRCode Layer到S3 Bucket
![image](https://hackmd.io/_uploads/HkwAHfpXT.png)
4.上傳結果
![image](https://hackmd.io/_uploads/SJmgUzpmp.png)
5.S3 URI
![image](https://hackmd.io/_uploads/By64fVAmp.png)
ex:s3://lambda-layer-2023-08-east-1/lambda-layer-qrcode.zip

## Lambda 增加Layer(QRCode)
1.AWS Console搜尋Lambda
![image](https://hackmd.io/_uploads/SkaoMM6QT.png)

2.點選Layer
![image](https://hackmd.io/_uploads/SJh47z6Xa.png)

3.按Create Layer
![image](https://hackmd.io/_uploads/rkNubERXp.png)

4.輸入相關設定值
![image](https://hackmd.io/_uploads/HyrFMVCmp.png)

S3 URI在這此查看
![image](https://hackmd.io/_uploads/S1T6w3AXa.png)

5.選擇Run Time
![image](https://hackmd.io/_uploads/BywpfEAma.png)

6.最後按Create
![image](https://hackmd.io/_uploads/S1NDPnCXa.png)




# 新增S3 Trigger Lambda
1.AWS Console中輸入Lambda
![image](https://hackmd.io/_uploads/HJQdPl6Xp.png)

2.執行Create Function
![image](https://hackmd.io/_uploads/HyHf_epXT.png)

3.Lambda組態設定
![image](https://hackmd.io/_uploads/HJZiuepma.png)

| Name          | Value                  |
| ------------- | ---------------------- |
| Function Name | S3-Image-UploadTrigger |
| Runtime       | Python 3.8                 |
| Execution Role | LabRole  |

輸入完成後按Create

4.設定執行Time Out
![image](https://hackmd.io/_uploads/BkXKqx6Qp.png)
按Edit會出現下列的畫面
![image](https://hackmd.io/_uploads/BypTcgTmp.png)
修改完成後按Save

5.程式碼如下
```python=
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

```
6.在Function Overview add trigger
![image](https://hackmd.io/_uploads/Bks22gpm6.png)

7.選擇S3
![image](https://hackmd.io/_uploads/Bk3balTma.png)

8.相關設定
S3 Bucket
![image](https://hackmd.io/_uploads/SJeyRl6Xp.png)
Event Type
![image](https://hackmd.io/_uploads/SJXX0eTQ6.png)
輸入Prefix:car_image/
![image](https://hackmd.io/_uploads/rJNnkZ6Q6.png)
設定完成後按Add

9.驗證Trigger Lambda是否正確執行 
上傳檔案到Bucket下的car_image/目錄
![image](https://hackmd.io/_uploads/SkDNEbpQp.png)
選擇圖檔並上傳之後
AWS Console切換到Cloud Watch看Log
![image](https://hackmd.io/_uploads/rJpWrZ6m6.png)
左邊選單選
Log groups
![image](https://hackmd.io/_uploads/B1jb8Z6Xa.png)
搜尋Log Group
![image](https://hackmd.io/_uploads/r1cTBZaXp.png)
查看Log Group中的輸出
![image](https://hackmd.io/_uploads/ryCcLba7p.png)

![image](https://hackmd.io/_uploads/rywjHWTQT.png)

7.Lambda增加文字辨識部分

程式碼如下
```python=
import json

import base64

import boto3

from datetime import datetime

import json

import base64

import boto3

from datetime import datetime

import os
 
import time

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
```
------------------------------------
每次改動Lambda之後都需要重新執行Deploy
------------------------------------

![image](https://hackmd.io/_uploads/rJacMd6Xp.png)

Cloud Watch驗證輸出
![image](https://hackmd.io/_uploads/Symepw6Q6.png)

8.增加寫入DynamoDB部分
```python=
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
```
Cloud Watch Output
![image](https://hackmd.io/_uploads/r1-yX_67p.png)
DynamoDB驗證是否有寫入(Explore Table Item)
![image](https://hackmd.io/_uploads/Bk3SX_6mp.png)
輸出結果
![image](https://hackmd.io/_uploads/B1bJ-_pm6.png)

# 新增QRCode Lambda
1.AWS Console中輸入Lambda
![image](https://hackmd.io/_uploads/HJQdPl6Xp.png)

2.執行Create Function
![image](https://hackmd.io/_uploads/HyHf_epXT.png)

3.Lambda組態設定
![image](https://hackmd.io/_uploads/BJGc8EA7p.png)
| Name          | Value                  |
| ------------- | ---------------------- |
| Function Name | GenQRCodeLambda |
| Runtime       | Python 3.8                 |
| Execution Role | LabRole  |

4.設定執行Time Out
![image](https://hackmd.io/_uploads/BkXKqx6Qp.png)
按Edit會出現下列的畫面
![image](https://hackmd.io/_uploads/BypTcgTmp.png)
修改完成後按Save

5.增加Layer
code/add layer
![image](https://hackmd.io/_uploads/ryF7dV07a.png)
![image](https://hackmd.io/_uploads/r1bH2VAQT.png)
最後按Add

6.設定環境變數
按Edit
![image](https://hackmd.io/_uploads/Sy4G7z0Xa.png)
輸入Bucket設定(S3儲存QRCode)
![image](https://hackmd.io/_uploads/SyGhpN0mp.png)



| Key         | Value |
| ----------- | ----- |
| BUCKET_NAME |  XXXXX     |


---------------------------------
其中xxxxx請改為新建立的Bucket Name
---------------------------------


7.程式碼如下
```python=
import json
import qrcode
import io
import os
import boto3

BUCKET_NAME = os.environ['BUCKET_NAME']


s3 = boto3.client('s3')

def lambda_handler(event, context):
    #text = event['pathParameters']['text']
    text = event['text']
    file_name_prefix = event['file_name_prefix']

    output = io.BytesIO()

    #dump text to json format
    image = qrcode.make(json.dumps(text))
    image.save(output)

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f'QRCode/{file_name_prefix}.png',
        Body=output.getvalue(),
    )

    return {
        'statusCode': 200,
    }
```
8.設定Test Event(單元測試)
![image](https://hackmd.io/_uploads/BJxS9zRQp.png)
輸入名稱跟設定值,確定之後按Save
![image](https://github.com/LabKCIS/ncnu-face-recognition/assets/187520/72352428-d034-4a70-868d-97600e23c3e5)


設定值範例

```=
{
  "text": "AWS Test",
  "file_name_prefix": "12345678"
}
```
| Name      | Description       |
| --------- | ----------------- |
| text      | QRCode Scan結果文字 |
| file_name_prefix | 圖檔檔名Prefix |
9.執行單元測試
![image](https://hackmd.io/_uploads/SyAvAhAQa.png)

S3 Console查看結果
![image](https://hackmd.io/_uploads/Sk8h4IRm6.png)





## 新增Line Notify Lambda
1.AWS Console中輸入Lambda
![image](https://hackmd.io/_uploads/HJQdPl6Xp.png)

2.執行Create Function
![image](https://hackmd.io/_uploads/HyHf_epXT.png)

3.Lambda組態設定
![image](https://hackmd.io/_uploads/HJZiuepma.png)

| Name          | Value                  |
| ------------- | ---------------------- |
| Function Name | SendLineNotify |
| Runtime       | Python 3.8                 |
| Execution Role | LabRole  |

輸入完成後按Create

4.設定執行Time Out
![image](https://hackmd.io/_uploads/BkXKqx6Qp.png)
按Edit會出現下列的畫面
![image](https://hackmd.io/_uploads/BypTcgTmp.png)
修改完成後按Save

5.程式碼如下
```python=
import urllib.request, json, ssl
import sys
import urllib.parse
import datetime
import os

LINE_TOKEN= os.environ.get("LINE_NOTIFY_API_KEY")
LINE_NOTIFY_URL="https://notify-api.line.me/api/notify"
S3_PREFIX=os.environ.get("S3_PREFIX")
S3_UPLOAD_IMG_PREFIX=os.environ.get("S3_UPLOAD_IMG_PREFIX")

def lineNotifyImage(msg, picurl):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    # 宣告一個物件，裡面存放要傳送的訊息
    payload = {
        'message': msg,
        # 縮圖
        'imageThumbnail': picurl,
        # 全圖
        'imageFullsize': picurl,
    }
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)
    

def lineNotify(msg):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": msg}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

def lambda_handler(event, context):
    status_code = 200
    #request_body = json.loads(event['body'])
    #concatenated_string = request_body['service']
    msg = "停車資訊"
    text = event['text']
    file_name = event['file_name']
    msg = text 
    picurl_temp = ''   
    print(event['type'])
    if event['type'] == 'qrcode':
        picurl_temp = S3_PREFIX + file_name
    else:
        picurl_temp = S3_UPLOAD_IMG_PREFIX + file_name   

    print(picurl_temp);
    picurl = "https://image-upload-2023-08.s3.ap-northeast-1.amazonaws.com/QRCode/12345678.png"
    lineNotifyImage(msg, picurl_temp)
    return { 
        'message' : msg
    } 
   


```
6.設定環境變數
按Edit
![image](https://hackmd.io/_uploads/Sy4G7z0Xa.png)
輸入三個設定
![image](https://hackmd.io/_uploads/SymJHMAXT.png)

| Key                    | Value                                     |
| ---------------------- | ----------------------------------------- |
| LINE\_NOTIFY\_API_KEY  | 申請的Line API Key                        |
| S3_PREFIX              | https://XXXXX.s3.amazonaws.com/QRCode/    |
| S3\_UPLOAD\_IMG_PREFIX | https://XXXXX.s3.amazonaws.com/car_image/ |


*其中xxxxx請改為新建立的Bucket Name*

Note:實際的HTTPS Link 請參考S3設定(下圖的Region是在美西)
![image](https://github.com/LabKCIS/ncnu-face-recognition/assets/187520/f2231d12-7302-4411-956d-4da6e62b8952)

7.設定Test Event(單元測試)
![image](https://hackmd.io/_uploads/BJxS9zRQp.png)
輸入名稱跟設定值,確定之後按Save
![image](https://hackmd.io/_uploads/SJcxjGA7a.png)
設定值範例
```=
{
  "text": "original_image", 
  "file_name": "car_no_sample.png",
  "type": "original"
}
```


| Name      | Description       |
| --------- | ----------------- |
| text      | Line Message Text |
| file_name | 圖檔名稱          |
| type      | original/qrcode(上傳原始圖檔/產生的QRCode)   |

8.執行單元測試
![image](https://hackmd.io/_uploads/HyhfAG0Xp.png)


9.Line Notify顯示結果
![image](https://hackmd.io/_uploads/BkOxRfA7p.png)


## S3 Trigger Lambda 呼叫QRCode/Line Notify Lambda
### QRCode部分
程式碼
```python=
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
    client = boto3.client('lambda')
    
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
    #generate QRCode
    accountid = context.invoked_function_arn.split(":")[4]
    region = context.invoked_function_arn.split(":")[3]  
    data_qrcode = {}
    data['car_no'] = textRekoResult
    data['file_name_prefix'] = created
 
    dataResponse = data
    
    inputParams = {
        "text"   : data,
        "file_name_prefix"      : created
    }    
    response = client.invoke(
        FunctionName = f'arn:aws:lambda:{region}:{accountid}:function:GenQRCodeLambda',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    ) 

    
    return {
        'statusCode': 200,
        'body': json.dumps(data) 
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
```
### LineNotify部分
----------------------------------------
Line Notify呼叫兩次
第一次顯示辨識結果/原始圖片
第二次顯示QR Code Message/產生的QRCode圖檔
----------------------------------------
程式碼
```
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
    client = boto3.client('lambda')
    
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
    #generate QRCode
    accountid = context.invoked_function_arn.split(":")[4]
    region = context.invoked_function_arn.split(":")[3]  
    data_qrcode = {}
    data['car_no'] = textRekoResult
    data['file_name_prefix'] = created
 
    dataResponse = data
    
    inputParams = {
        "text"   : data,
        "file_name_prefix"      : created
    }    
    response = client.invoke(
        FunctionName = f'arn:aws:lambda:{region}:{accountid}:function:GenQRCodeLambda',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )   

    #sent line notify(with reko result)
    data = {}
    car_image_path = file_name
    car_image_path_array = car_image_path.split("/")
    car_image_name = car_image_path_array[-1]    
    data['type'] = "original"
    data['text'] = "Parking_info/Identify Result:" + textRekoResult
    data['file_name'] = car_image_name
    
    inputParams = {
        "text"   : data['text'],
        "file_name" : data['file_name'],
        "type" : data['type']
    } 
    response = client.invoke(
        FunctionName = f'arn:aws:lambda:{region}:{accountid}:function:SendLineNotify',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )        

    #sent line notify(with qrcode)
    data = {}

    data['type'] = "qrcode"
    data['text'] = "paying_qrcode"
    data['file_name'] = str(created) +".png"
    
    inputParams = {
        "text"   : data['text'],
        "file_name" : data['file_name'],
        "type" : data['type']
    } 
    response = client.invoke(
        FunctionName = f'arn:aws:lambda:{region}:{accountid}:function:SendLineNotify',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )     
    return {
        'statusCode': 200,
        'body': json.dumps(data) 
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
```
Line Notify結果如下

![image](https://hackmd.io/_uploads/S18lu8R76.png)

![image](https://hackmd.io/_uploads/rkdZ_L0m6.png)

# Revise By GPT
Prompt:請用易於維護,更容易理解的角度修改此Python
修改結果:
```
import json
import base64
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError

# 環境變量
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
GEN_QRCODE_LAMBDA = os.environ['GEN_QRCODE_LAMBDA']
SEND_LINE_NOTIFY_LAMBDA = os.environ['SEND_LINE_NOTIFY_LAMBDA']

# 初始化 AWS 服務客戶端
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
rekognition_client = boto3.client('rekognition')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        # 從 S3 事件中獲取資訊
        bucket_name, file_name = get_s3_info(event)
        print(f'Processing file: {file_name} from bucket: {bucket_name}')

        # 執行 OCR
        car_number = perform_ocr(bucket_name, file_name)

        # 生成時間戳
        timestamp = int(datetime.now().timestamp())

        # 插入 DynamoDB
        insert_parking_record(timestamp, car_number, file_name)

        # 生成 QR 碼
        generate_qr_code(car_number, timestamp)

        # 發送 Line 通知
        send_line_notifications(car_number, file_name, timestamp)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Processing completed successfully', 'car_number': car_number})
        }
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_s3_info(event):
    """從 S3 事件中提取桶名和檔案名"""
    s3_event = event['Records'][0]['s3']
    return s3_event['bucket']['name'], s3_event['object']['key']

def perform_ocr(bucket_name, file_name):
    """使用 Rekognition 進行 OCR"""
    try:
        response = rekognition_client.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': file_name}})
        detected_texts = response['TextDetections']
        
        # 假設我們只需要第一個檢測到的文本
        if detected_texts:
            return detected_texts[0]['DetectedText']
        else:
            raise ValueError("No text detected in the image")
    except ClientError as e:
        print(f"Error in OCR: {e}")
        raise

def insert_parking_record(timestamp, car_number, file_name):
    """向 DynamoDB 插入停車記錄"""
    table = dynamodb.Table(DYNAMODB_TABLE)
    try:
        response = table.put_item(
            Item={
                'created': timestamp,
                'car_no': car_number,
                'enter_image': file_name,
                'exit_image': "None",
                'exit_time': 0,
                'status': 'enter'
            }
        )
        print(f"DynamoDB insert response: {response}")
    except ClientError as e:
        print(f"Error inserting into DynamoDB: {e}")
        raise

def generate_qr_code(car_number, timestamp):
    """調用 QR 碼生成 Lambda"""
    try:
        payload = {
            "text": {"car_no": car_number},
            "file_name_prefix": timestamp
        }
        lambda_client.invoke(
            FunctionName=GEN_QRCODE_LAMBDA,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
    except ClientError as e:
        print(f"Error invoking QR code Lambda: {e}")
        raise

def send_line_notifications(car_number, file_name, timestamp):
    """發送 Line 通知"""
    try:
        # 發送原始圖像通知
        send_notification({
            "text": f"Parking_info/Identify Result: {car_number}",
            "file_name": file_name.split("/")[-1],
            "type": "original"
        })

        # 發送 QR 碼通知
        send_notification({
            "text": "paying_qrcode",
            "file_name": f"{timestamp}.png",
            "type": "qrcode"
        })
    except ClientError as e:
        print(f"Error sending Line notifications: {e}")
        raise

def send_notification(payload):
    """調用 Line Notify Lambda"""
    lambda_client.invoke(
        FunctionName=SEND_LINE_NOTIFY_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
```
輸入三個設定


![image](https://hackmd.io/_uploads/HyTdHSdnC.png)

| Key | Value  |
|-|-|
| DYNAMODB_TABLE | car_parking  |
| GEN\_QRCODE\_LAMBDA | GenQRCodeLambda  |
| SEND\_LINE\_NOTIFY_LAMBDA | SendLineNotify  |

主要的改進包括：

1. **模組化**：將不同的功能分解為獨立的函數，每個函數負責一個特定的任務。

2. **錯誤處理**：在每個函數中添加了異常處理，以捕獲和記錄特定的錯誤。

3. **使用環境變量**：將配置信息（如表名和其他 Lambda 函數名）移到環境變量中。

4. **註釋**：為每個函數添加了 docstring，解釋其功能。

5. **一致的命名**：使用更一致和描述性的變量名。

6. **簡化邏輯**：例如，在 OCR 函數中，我們假設只需要第一個檢測到的文本。

7. **提前初始化客戶端**：在全局範圍內初始化 AWS 服務客戶端，以便在 Lambda 容器重用時提高效率。
