from django.apps import AppConfig

class SendGmailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'send_gmail'

    def ready(self):
        import send_gmail.signals  # 导入信号模块
