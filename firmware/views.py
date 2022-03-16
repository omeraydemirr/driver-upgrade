    
#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################


from django_fields import *
from django.http import JsonResponse
from django.core.files.storage import  FileSystemStorage
from firmware.forms import *
from django.shortcuts import render, HttpResponse
from boto3.dynamodb.conditions import Key, Attr
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.files import File
from urllib.parse import parse_qs
from django.contrib.sessions.backends.file import *
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sessions import *
from django.contrib.sessions.backends.signed_cookies import *
from soft import settings
from botocore.exceptions import ClientError
import json , boto3 ,base64 , datetime , os , urllib3 , csv, codecs , hashlib ,hmac

########################
###### GET DynamoDB TABLES AND S3 BUCKET NAMES ######
########################
def device_info_table(request):

    try:
        client = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['REGION_NAME'],
    )
        table = client.Table('DeviceInfo')
        return table
    except:
        return False

def driver_info_table(request):

    try:
        client = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ['REGION_NAME'],
        )
        table = client.Table('DriverInfo')
        return table
    except:
        return False


def s3_bucket(request):
    try:
        client = boto3.resource(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['REGION_NAME'],
        )
        return client
    except:
        return False

################################################################


########################
###### INDEX VIEW ######
########################
def home_view(request):
    #IF NEEDED AUTHENTICATION
    # token_value = request.session.get('AccessToken')
    # if not token_value:

    return render(request, 'intro.html')


########################
###### QUERY FUNCTIONS ######
########################
def get_vendors(request):
    try:
        table = device_info_table(request)
        response = table.scan(
                ProjectionExpression='vendor'
            )
    except Exception as e:
        print(e)
        return []
    else:
        if "Items" in response:
            response = response["Items"]
            response = list({v['vendor']: v['vendor'] for v in response}.values())
        return response

def get_s3_drivers(request,vendor,device,model,op_s,series):
    s3 = s3_bucket(request).meta.client
    keys = []
    try:
        response = s3.list_objects_v2(
            Bucket=os.environ['BUCKET'],
            Prefix=vendor + '/' + device + '/' + model + '/' + op_s
        )
    except Exception as e:
        print(e)
    else:
        if 'Contents' in response:
        
            objs = response['Contents']
            get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
            keys = [obj["Key"].rsplit('/',1)[-1] for obj in sorted(objs, key=get_last_modified, reverse=True)][0:10]
    return keys

def filter_device_with_vendor(request,vendor):
    if vendor != '':
        try:
            table = device_info_table(request)
            response = table.query(
                    IndexName='vendor-idx',
                    KeyConditionExpression=Key("vendor").eq(vendor),
                    ProjectionExpression='device'
                )
        except Exception as e:
            print(e)
            return []
        else:
            if "Items" in response:
                response = response["Items"]
                response = list({v['device']: v['device'] for v in response}.values())
            return response
    else:
        return []

def filter_model_with_vendor_and_device(request,vendor,device):
    try:
        table = device_info_table(request)
        response = table.query(
                IndexName='vendor-idx',
                KeyConditionExpression=Key("vendor").eq(vendor) & Key("device").eq(device) ,
                ProjectionExpression='model'
            )
    except Exception as e:
        print(e)
        return []
    else:
        if "Items" in response:
            response = response["Items"]
            response = list({v['model']: v['model'] for v in response}.values())    
        return response



def filter_os(request,vendor,device,model):
    try:
        table = device_info_table(request)
        response = table.query(
                IndexName='vendor-idx',
                KeyConditionExpression=Key("vendor").eq(vendor) & Key("device").eq(device) ,
                ProjectionExpression='os'
            )
    except Exception as e:
        print(e)
        return []
    else:
        if "Items" in response:
            response = response["Items"]
            response = list({v['os']: v['os'] for v in response}.values())    
        return response

def filter_series(request,vendor,device,model,os):
    try:
        items = str([vendor,device,model,os])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
        table = driver_info_table(request)
        response = table.query(
            KeyConditionExpression=Key("id").eq(item_id),
            ProjectionExpression="series",
            )
    except Exception as e:
        print(e)
        return []
    else:
        if "Items" in response:
            response = response["Items"]
            response = list({v['series']: v['series'] for v in response}.values())    
        return response

def series_info(request,vendor,device,model,os,series):
    try:
        items = str([vendor,device,model,os])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
        table = driver_info_table(request)
        response = table.query(
            KeyConditionExpression=Key("id").eq(item_id) & Key("series").eq(series),
            ProjectionExpression="firmware,last_upgrade_time",
            )
    except Exception as e:
        print(e)
        return []
    else:
        if "Items" in response:
            response = response["Items"]
            fw_response = list({v['firmware']: v['firmware'] for v in response}.values())   
            time_response = list({v['last_upgrade_time']: v['last_upgrade_time'] for v in response}.values())
        return fw_response,time_response


def create_driver_item(request,item_id,vendor,device,model,os):
        try:
            table = device_info_table(request)
            put_response = table.put_item(
                            Item={
                                'id': item_id ,
                                'vendor': vendor,
                                'device': device,
                                'model': model,
                                'os':os
                            },
                            ConditionExpression='attribute_not_exists(id)',
                        
                        )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                pass
            else:
                print(e)
                return False           
        else:
            return put_response


def create_firmware_item(request,item_id,series):
    try:
        table = driver_info_table(request)
        put_response = table.put_item(
                        Item={
                            'id': item_id ,
                            'series': series,
                            'firmware': "empty",
                            'last_upgrade_time':0,
                        },
                        ConditionExpression='attribute_not_exists(id)',
                    
                    )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        else:
            print(e)
            raise       
    else:
        return put_response

def update_firmware_item(request,item_id,series,file_name,timestamp):
    try:
        table = driver_info_table(request)
        put_db = table.update_item(
                Key={
                    'id':item_id,
                    'series':series,
                },
                UpdateExpression = "set firmware=:n,last_upgrade_time=:a",
                ExpressionAttributeValues = {':n': file_name,':a':timestamp},
                ReturnValues = "UPDATED_NEW")
    except Exception as e:
        print(e)
        raise
    else:
        return JsonResponse({"success": True}, status=200)

def delete_firmware_item(request,item_id,series):
    try:
        table = driver_info_table(request)
        put_db = table.update_item(
                Key={
                    'id':item_id,
                    'series':series,
                },
                UpdateExpression = "set firmware=:n",
                ExpressionAttributeValues = {':n': "empty",},
                ReturnValues = "UPDATED_NEW")
    except Exception as e:
        print(e)
        raise
    else:
        return JsonResponse({"success": True}, status=200)


def select_items(request):
    option = request.GET.get('option','')
    vendor = request.GET.get('vendor','')
    device = request.GET.get('device','')
    model = request.GET.get('model','')
    os = request.GET.get('os','')
    series = request.GET.get('series','')
    
    if option == 'vendor':
        devices = filter_device_with_vendor(request,vendor)
        return JsonResponse({'devices':devices})
    elif option == 'device':
        models = filter_model_with_vendor_and_device(request,vendor,device)
        return JsonResponse({'models':models})
    elif option == 'model':
        os_items = filter_os(request,vendor,device,model)
        return JsonResponse({'operating_systems':os_items})
    elif option == 'os':
        serieses = filter_series(request,vendor,device,model,os)
        return JsonResponse({'serieses':serieses})
    elif option == 'series':
        if series != None:
            firmware,last_upgrade_time = series_info(request,vendor,device,model,os,series)
            s3_drivers = get_s3_drivers(request,vendor,device,model,os,series)
            return JsonResponse({"firmware":firmware, "last_upgrade_time":last_upgrade_time, "drivers":s3_drivers})
        else:
            return JsonResponse({"firmware":[], "last_upgrade_time":[], "drivers":[]})

def get_driver(request,item_id,series):
    try:
        table = driver_info_table(request)
        response = table.query(
            KeyConditionExpression=Key("id").eq(item_id) & Key("series").eq(series),
            ProjectionExpression="firmware",
            )
    except Exception as e:
        print(e)
    else:
        if "Items" in response:
            response = response["Items"][0]["firmware"]
        return response


def delete_series_item(request,item_id,series):
    driver_table = driver_info_table(request)
    try:
        delete_series_item = driver_table.delete_item(
            Key={
                    'id': item_id,
                    'series':series
                },
        )
        return JsonResponse({"success": True}, status=200)
    except:
        raise


    
#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################



########################
###### UPLOAD DRIVER,ADD SERIES,DOWNLOAD DRIVER,
# DELETE FIRMWARE AND DELETE SERIES FUNCTIONS ######
########################
def upload_file(request):
    form = FirmwareForm()
    table = driver_info_table(request)
    vendors = get_vendors(request)

    client = s3_bucket(request).meta.client

    vendor = request.POST.get('vendor','')
    device = request.POST.get('device','')
    model = request.POST.get('model','')
    operating_system = request.POST.get('os','')
    series = request.POST.get('series','')
    items = str([vendor,device,model,operating_system])
    item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
    now = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(now))
    if request.FILES and request.method == 'POST':
        local_file = request.FILES["file"]
        file_size = local_file.size 
        file_name = local_file.name

        try:

            #IF File is smaller than 5 mb
            if file_size < 5242880:
                try:
                    folder_name = vendor + '/' + device + '/' + model + '/' + operating_system + '/' + series + '/' + file_name
                    client.put_object(Body=local_file.read(),Bucket=os.environ['BUCKET'],Key=folder_name,ContentType=local_file.content_type)
                except Exception as e:
                    print(e)
                    raise
            else:
                try:
                    folder_name = vendor + '/' + device + '/' + model + '/' + operating_system + '/' + series + '/' + file_name
                    temp_dir =  "./bin/temp/"
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    fs = FileSystemStorage(location=temp_dir)
                    fs.save(local_file.name, local_file)
                    local_file_dir = temp_dir + local_file.name
                    client.upload_file(local_file_dir, os.environ['BUCKET'], folder_name)

                except Exception as e:
                    os.remove(local_file_dir)
                    print(e)
                    raise
                else:
                    os.remove(local_file_dir)
        except Exception as e:
            print(e)
            raise
        else:

            update_firmware_item(request,item_id,series,file_name,timestamp)
    elif not request.FILES and request.method == 'POST':
        file_list = request.POST.get('file','')
        updated_item = update_firmware_item(request,item_id,series,file_list,timestamp)

    return render(request, 'uploadform.html',{'form': form , 'vendors':vendors},status=200)



def create_driver_element(request):

    form = FirmwareForm()
    vendors = get_vendors(request)

    if request.method == 'POST' and not request.FILES:
        vendor = request.POST.get('vendor', None)
        device = request.POST.get('device', None)
        model = request.POST.get('model', None)
        os = request.POST.get('os', None)
        series = request.POST.get('series',None)
        items = str([vendor,device,model,os])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8") 
        try:
            driver_response = create_driver_item(request,item_id,vendor,device,model,os)
            if driver_response != False:
                firmware_response = create_firmware_item(request,item_id,series)
                if firmware_response == False:
                    return JsonResponse({'error':'The item is already exists'},status=409)
        except Exception as e:
            print(e)
            return JsonResponse({'error':'Something went wrong!'},status=400)
        else:
            return JsonResponse({'success':'Items created in db successfully'},status=200)
    elif request.FILES and request.method == 'POST':
        try:
            local_file = request.FILES['file']
            reader = csv.DictReader(codecs.iterdecode(local_file, 'utf-8'))
            for rows in list(reader):
                vendor = rows['vendor']
                device = rows['device']
                model = rows['model']
                os = rows['os']
                series = rows['series']
                items = str([vendor,device,model,os])
                item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8") 
                driver_response = create_driver_item(request,item_id,vendor,device,model,os)
                if driver_response != False:
                    firmware_response = create_firmware_item(request,item_id,series)
                    if firmware_response == False:
                        pass
        except Exception as e:
            print(e)
            return JsonResponse({'error':'Something went wrong!'},status=400)
        else:
            return JsonResponse({'success':'Items created in db successfully'},status=200)
    return render(request, 'device_form.html',
                      {'form':form,'vendors':vendors}, status=200)


def download_driver(request):
    form = FirmwareForm()
    vendors = get_vendors(request)
    client = s3_bucket(request)


    if request.POST or request.method == "POST":
        query_string = str(request.body,"utf-8")
        json_query =  json.loads(json.dumps(parse_qs(query_string)))
        vendor = json_query["vendor"][0]
        device = json_query["device"][0]
        model = json_query["model"][0]
        operating_system = json_query["os"][0]
        series = json_query["series"][0]
        items = str([vendor,device,model,operating_system])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
        driver = get_driver(request,item_id,series)
        folder_name = vendor + '/' + device + '/' + model + '/' + operating_system + '/' + series + '/' + driver
        bucket = os.environ['BUCKET']
        #download_folder = "./bin/temp/" + driver
        try:
            get_obj = client.get_object(Bucket=bucket,Key=folder_name)
            content_type = get_obj["ContentType"]
            file_read = get_obj['Body'].read()
            return HttpResponse(file_read,content_type)
        except:
            raise          
    return render(request,"download.html",{'form':form ,"vendors":vendors})

    
def delete_driver(request):
    form = FirmwareForm()
    vendors = get_vendors(request)
    if request.method == 'POST' and not request.FILES:
        vendor = request.POST.get('vendor', None)
        device = request.POST.get('device', None)
        model = request.POST.get('model', None)
        os = request.POST.get('os', None)
        series = request.POST.get('series',None)
        items = str([vendor,device,model,os])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
        delete_driver = delete_firmware_item(request,item_id,series)

    return render(request,"deletedriver.html",{'form':form,"vendors":vendors})

def delete_series(request):
    form = FirmwareForm()
    vendors = get_vendors(request)
    if request.method == 'POST' and not request.FILES:
        vendor = request.POST.get('vendor', None)
        device = request.POST.get('device', None)
        model = request.POST.get('model', None)
        os = request.POST.get('os', None)
        series = request.POST.get('series',None)
        items = str([vendor,device,model,os])
        item_id = str(base64.b64encode(bytes(items,"utf-8")),"utf-8")
        delete_driver = delete_series_item(request,item_id,series)
    return render(request,"deleteseries.html",{'form':form,"vendors":vendors})

#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################


########################
###### CREATE TABLES AND BUCKETS WHEN SERVER IS STARTED TO RUNNING ######
########################
def create_tables(request):

    #CHECK AND CREATE S3 BUCKET
    s3_bucket = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['REGION_NAME'],
    )
    try:
        s3_bucket.head_bucket(Bucket=os.environ["BUCKET"])
    except Exception as e:
        if e.response["Error"]["Code"] == "404":
            try:
                print("S3 BUCKET IS CREATING NOW...")
                response = s3_bucket.create_bucket(
                ACL='private',
                Bucket=os.environ["BUCKET"],
                CreateBucketConfiguration={
                    'LocationConstraint': os.environ["REGION_NAME"]
                },
            )
            except Exception as e:
                if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                    print("S3 BUCKET ALREADY EXISTS")
                else:
                    print("SOMETHING WENT WRONG!")
            else:
                print("BUCKET CREATED SUCCESSFULLY!")



    #CHECK AND CREATE TABLES
    dynamodb = boto3.resource('dynamodb',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['REGION_NAME'],)

    table_names = [table.name for table in dynamodb.tables.all()]

    if "DeviceInfo" not in table_names:
        try:
            print("DEVICE TABLE IS CREATED NOW...")
            device_table = dynamodb.create_table(
                TableName='DeviceInfo',
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'vendor',
                        'KeyType': 'RANGE'  # Sort key
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'vendor',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'device',
                        'AttributeType': 'S'
                    },



                ],
                GlobalSecondaryIndexes=[
                    {
                'IndexName': 'vendor-idx',
                'KeySchema': [
                    {
                        'AttributeName': 'vendor',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName':'device',
                        'KeyType': 'RANGE'
                    }
                ],
                
                'Projection': {
                    'ProjectionType': 'ALL',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
                },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print("DEVICE TABLE IS CREATED SUCCESSFULLY!")
        except Exception as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":        
                print("DEVICE INFO TABLE ALREADY EXISTS")
            else:
                print("SOMETHING WENT WRONG!")
                pass
    
    if "DriverInfo" not in table_names:
        try:
            print("DRIVER TABLE IS CREATED NOW...")
            driver_table = dynamodb.create_table(
            TableName='DriverInfo',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'series',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'series',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
            print("DRIVER TABLE IS CREATED SUCCESSFULLY!")
        except Exception as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":        
                print("DRIVER INFO TABLE ALREADY EXISTS")
            else:
                print("SOMETHING WENT WRONG!")
    
#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################


########################
###### EXTRA AUTH FUNCTIONS FOR COGNITO ######
########################

def loginpage(request):
    return render(request,'loginpage.html')


# def get_secret_hash(username):
#     msg = username + CLIENT_ID
#     dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
#         msg = str(msg).encode('utf-8'),   digestmod=hashlib.sha256).digest()
#     secrethash = base64.b64encode(dig).decode()
#     return secrethash

# def initiate_auth(request):
#     if request.method == 'POST':
#         username = request.POST.get('login_username')
#         password = request.POST.get('login_password')
#         client = boto3.client("cognito-idp", region_name="eu-central-1")
#         # Initiating the Authentication, 
#         response = client.initiate_auth(
#             ClientId=CLIENT_ID,
#             AuthFlow="USER_PASSWORD_AUTH",
#             AuthParameters={"USERNAME": username, 
#             'SECRET_HASH': get_secret_hash(username),
#             "PASSWORD": password},
#         )

#         # From the JSON response you are accessing the AccessToken
#         print(response)
#         # Getting the user details.
#         access_token = response["AuthenticationResult"]["AccessToken"]

#         response = client.get_user(AccessToken=access_token)
#         print(response)

