# S3 Event Trigger With Lambda(縮圖)


## 程式範例請到下列的網址下載

https://s3-us-west-2.amazonaws.com/us-west-2-aws-training/awsu-spl/spl-88/2.3.15.prod/scripts/CreateThumbnail.zip

## S3建立Source/Target Bucket


| Bucket Name | Type |
| -------- | -------- |
| XXXXX         |   Source       |
| XXXXX-resized     | Destination     |

## 建立縮圖Lambda
### AWS Console 搜尋Lambda

### 點擊Create function
![image](https://hackmd.io/_uploads/HkpBrukEp.png)
### 輸入設定值
![image](https://hackmd.io/_uploads/HJ6l8dk4p.png)
設定值如下
| Name          | Value                  |
| ------------- | ---------------------- |
| Function Name | image-resize |
| Runtime       | Python 3.7                 |
| Execution Role | LabRole  |

### 上傳程式碼
![image](https://hackmd.io/_uploads/BkiSvukNp.png)
選擇要上傳的zip file
![image](https://hackmd.io/_uploads/HkXFvu1V6.png)
![image](https://hackmd.io/_uploads/BJB2v_146.png)
按Save上傳
![image](https://hackmd.io/_uploads/S11yd_1V6.png)

### 修改Lambda設定
#### Runtime settings
點擊Edit
![image](https://hackmd.io/_uploads/HkOwuu146.png)
修改Handler為
CreateThumbnail.handler 
![image](https://hackmd.io/_uploads/r18lKukVT.png)
並點擊Save

### Lambda 設定Trigger
![image](https://hackmd.io/_uploads/ByPKYu14p.png)
#### 選擇S3(從哪一個Bucket發動)
![image](https://hackmd.io/_uploads/SJtBJYyNT.png)
#### 設定Event Type
![image](https://hackmd.io/_uploads/S1cOJY1E6.png)
最後按Add
![image](https://hackmd.io/_uploads/r1e31KyET.png)

#### 上傳範例圖檔
點擊Upload
![image](https://hackmd.io/_uploads/r1QHet14p.png!)
點擊Add files
![image](https://hackmd.io/_uploads/Sy2deFkNT.png)
選取要上傳的檔案,按開啟
![image](https://hackmd.io/_uploads/SyFQbK1Na.png)
確定按Upload
![image](https://hackmd.io/_uploads/Hk-DZKyVa.png)
系統提示上傳成功
![image](https://hackmd.io/_uploads/HyAh-Ky4p.png)

#### 查看縮圖結果

![image](https://hackmd.io/_uploads/SJLfNF14T.png)








