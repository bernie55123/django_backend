from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    obj_user = models.ForeignKey(User, on_delete = models.CASCADE)
    jwt_token = models.CharField(max_length = 400)
    description = models.CharField(max_length = 400, default = None, blank = True, null = True)

class trade_request(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True,unique=True,verbose_name = 'email')
    balance = models.IntegerField(default=0 ,verbose_name = '時間餘額')
    task_name = models.CharField(default=None ,max_length = 30 ,null=True ,verbose_name = '任務名稱')
    task_cost = models.IntegerField(default=0 ,verbose_name = '任務時長')
    now_people = models.IntegerField(default=0,verbose_name = '現在人數')
    max_people = models.IntegerField(default=0,verbose_name = '總人數')
    point_limit = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(limit_value=100)],blank=False,verbose_name='積分限制')
    description_limit = models.TextField(default=None ,null= True ,blank = True ,verbose_name = '專長限制')
    task_info = models.TextField(default=None ,null= True ,blank = True ,verbose_name = '任務內容')
    thumbnail = models.TextField(blank = True,verbose_name="圖片路徑")
    result = models.CharField(max_length= 10000 ,null = True , default=None , verbose_name = '解果' , choices=[('None', ' '),('True', '通過'), ('False', '不通過')])
    
class id_info(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True,verbose_name = 'email')
    balance = models.IntegerField(default=0 ,verbose_name = '時間餘額')