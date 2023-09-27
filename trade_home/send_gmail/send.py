from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import os.path
import json,requests
from google_auth_oauthlib.flow import InstalledAppFlow
from .models import trade_request,id_info



# 設定要存取的範圍
SCOPES = ['https://mail.google.com/']

#向前端發布任務
"""def create_trade_mission(sender):
    uuid = "00000001"
    email = sender.id
    type = "1"
    name = sender.task_name  # 任務名稱
    overview = sender.task_info  # 任務概述
    token = sender.task_cost  # 任務時長
    cover = "your_cover_data_here"  # 這裡應該是你的任務封面數據

    url = f"{HOST_URL_TPLANET_DAEMON}/tasks/new"
    data = {
        "uuid": uuid,
        "email": email,
        "type": type,
        "name": name,
        "token": token,
        "overview": overview,
        "cover": cover
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Request successful")
        print(response.json())
        
    else:
        print("Request failed")
        print(response.status_code)
"""

#交易上鍊
def trade_chain(sender):
    url = "https://poe.townway.com.tw/iota/message"
    balance = sender.balance
    task_name = sender.task_name
    task_cost = sender.task_cost
    task_info = sender.task_info
    result = sender.result
    new_balance = balance-task_cost
    task = json.dumps({"id":sender.id, "balance":balance, "task_name":task_name,
        "task_cost":task_cost,"task_info":task_info,"result":result,"new_balance":new_balance})

    payload = json.dumps({
     "message": task
    })
    headers = {
    'Authorization': 'Basic Z2VvOjJ1bGlkZ29v',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()
    message_trace = response_data.get("explorer")
    return message_trace,new_balance

#扣除balance
def decrease_balance(sender):
    balance_record = id_info.objects.get(id=sender.id)
    balance_record.balance-=sender.task_cost
    balance_record.save()

#建立信件信息
def create_message(from_email, to_email, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

#寄送信件
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"郵件已成功寄出，郵件 ID: {message['id']}")
        return message
    except Exception as e:
        print(f"寄送郵件時發生錯誤: {e}")
        return None


def send_email(sender):
    # 載入憑證檔案
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('gmail', 'v1', credentials=creds)

    # 設定寄件者和收件者的電子郵件地址
    id = sender.id # 擷取目標信箱
    from_email = 'usr.isucsie@gmail.com'

    # 目標郵件位址
    to_email = sender.id

    # result:交易結果
    result = sender.result

    if result == 'True':
        message_trace,new_balance = trade_chain(sender)
        decrease_balance(sender)
        subject = '審核通過!(請勿回覆)'
        message_text = '恭喜你!\n你的交易結果已經通過審核了。\n相信您所兌換的服務很快就會有志工領取。\n交易相關內容已上鍊:'+message_trace
        id_info.objects.filter(id=sender.id).update(balance=new_balance)
        trade_request.objects.filter(id=sender.id).delete()
    elif result == 'False':
        subject = '審核未通過!(請勿回覆)'
        message_text = '非常遺憾\n你的交易結果未通過審核,請您重新申請。\n網址 : (https://beta-pure.townway.com.tw)。'
        trade_request.objects.filter(id=sender.id).delete()
    else :
        subject = '正在審核!(請勿回覆)'
        message_text = '恭喜你\n你的交易請求已送出,請耐心等候管理員審核。\n後續結果將以信件通知,屆時請關注信箱。'
    message = create_message(from_email, to_email, subject, message_text)
    send_message(service, 'me', message)