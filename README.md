# django_backend
1.create_request.py
        是前端交易所頁向後端發起交易請求並在資料庫建立一筆請求資料
2.send.py
        create_message()是建立信件信息,send_message()發送信件,send_email()設定信件
3.signals.py是信號機
        result_change_send_gmail()是用來偵測結果改變時觸發
        trade_send_backend()是用來偵測交易請求被建立時觸發
4.models.py是資料庫
        id:申請人gmail
        balance:時間餘額
        task_name:任務名稱
        task_cost:兌換時數
        tack_info:任務內容
        result:審核結果
