from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from .models import trade_request



# 設定要存取的範圍
SCOPES = ['https://mail.google.com/']

def create_message(from_email, to_email, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

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
    to_email = id

    # result:交易結果
    result = trade_request.objects.get(id=id).result

    if result == 'True':         
        subject = '審核通過!(請勿回覆)'
        message_text = '恭喜你!\n你的交易結果已經通過審核了。\n相信您所兌換的服務很快就會有志工領取。\n交易相關內容已上鍊'
    elif result == 'False':
        subject = '審核未通過!(請勿回覆)'
        message_text = '非常遺憾\n你的交易結果未通過審核,請您重新申請。\n網址 : (https://beta-pure.townway.com.tw)。'
    else :
        subject = '正在審核!(請勿回覆)'
        message_text = '恭喜你\n你的交易請求已送出,請耐心等候管理員審核。\n後續結果將以信件通知,屆時請關注信箱。'


    
    message = create_message(from_email, to_email, subject, message_text)
    send_message(service, 'me', message)


