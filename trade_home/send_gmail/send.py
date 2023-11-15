from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import os.path
import json,requests
from google_auth_oauthlib.flow import InstalledAppFlow
from .models import trade_request,Profile
from django.contrib.auth.models import User



# 設定要存取的範圍
SCOPES = ['https://mail.google.com/']

#向前端發布任務
def create_trade_mission(sender):
    uuid = "00000001"
    email = "400@gmail.com"
    type = "1"
    name = sender.task_name  # 任務名稱
    token = sender.task_cost  # 任務時長
    people_limit = sender.max_people #人數限制
    point_limit = sender.point_limit #積分限制
    description_limit = sender.description_limit #專長限制
    overview = sender.task_info  # 任務內容
    cover = sender.img  # 圖片

    url = "https://beta-tplanet-backend.townway.com.tw/tasks/new"
    data = {
        "uuid" : uuid,
        "email" : email,
        "type" : type,
        "name" : name,
        "token" : token,
        "people" : people_limit,
        "point" : point_limit,
        "description" : description_limit,
        "overview" : overview,
        "cover" : cover
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Request successful")
        print(response.json())
        
    else:
        print("Request failed")
        print(response.status_code)


#交易上鍊
def trade_chain(sender):
    url = "https://alfred.townway.com.tw/iota/message"
    balance = sender.balance
    task_name = sender.task_name
    task_cost = sender.task_cost
    people_limit = sender.max_people
    point_limit = sender.point_limit
    description_limit = sender.description_limit
    task_info = sender.task_info
    result = sender.result
    new_balance = balance-task_cost
    task = json.dumps({"id":sender.obj_user, "balance":balance, "task_name":task_name,
        "task_cost":task_cost,"task_info":task_info,"people_limit":people_limit,"point_limit":point_limit,"description_limit":description_limit,"result":result,"new_balance":new_balance})

    payload = json.dumps({
     "message": task
    })
    headers = {
    'Authorization': 'Basic Z2VvOjJ1bGlkZ29v',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()
    message_trace = 'https://explorer.iota.org/mainnet/block/'+response_data[0]
    return message_trace,new_balance

#建立信件信息
def create_message(from_email, to_email, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

#寄送信息
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"郵件已成功寄出，郵件 ID: {message['id']}")
        return message
    except Exception as e:
        print(f"寄送郵件時發生錯誤: {e}")
        return None


#寄送信件
def send_email(sender):
    # 載入憑證檔案
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('gmail', 'v1', credentials=creds)

    # 設定寄件者的電子郵件地址
    from_email = 'usr.isucsie@gmail.com'

    # result:交易結果
    result = sender.result

    if result == 'True':
        message_trace,new_balance = trade_chain(sender)
        create_trade_mission(sender)
        subject = '審核通過!(請勿回覆)'
        message_text = '恭喜你!\n你的交易結果已經通過審核了。\n相信您所兌換的服務很快就會有志工領取。\n交易相關內容已上鍊:'+ message_trace
        obj_user = User.objects.filter(email = sender.obj_user).get()
        Profile.objects.filter(obj_user=obj_user.id).update(balance=new_balance)
        trade_request.objects.filter(obj_user=sender.obj_user).delete()
    elif result == 'False':
        subject = '審核未通過!(請勿回覆)'
        message_text = '非常遺憾\n你的交易結果未通過審核,請您重新申請。\n網址 : (https://beta-pure.townway.com.tw)。'
        trade_request.objects.filter(obj_user=sender.obj_user).delete()
    else :
        subject = '正在審核!(請勿回覆)'
        message_text = '恭喜你\n你的交易請求已送出,請耐心等候管理員審核。\n後續結果將以信件通知,屆時請關注信箱。'
    message = create_message(from_email, sender.obj_user, subject, message_text)
    send_message(service, 'me', message)