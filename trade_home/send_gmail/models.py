from django.db import models


# Create your models here.
class trade_request(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    balance = models.PositiveIntegerField(verbose_name = '時間餘額')
    task_name = models.CharField(default=None ,max_length = 30 ,null=True ,verbose_name = '任務名稱')
    task_cost = models.IntegerField(default=0 ,verbose_name = '任務時長')
    task_info = models.TextField(default=None ,null= True ,blank = True ,verbose_name = '任務內容')
    result = models.CharField(max_length= 10000 ,null = True , default=None , verbose_name = '解果' , choices=[('None', ' '),('True', '通過'), ('False', '不通過')])
class id_info(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    balance = models.IntegerField(default=0 ,verbose_name = '時間餘額')