from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class trust_point(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    trust_point = models.PositiveIntegerField(default=100,validators=[MaxValueValidator(limit_value=100)],blank=False,verbose_name='信用積分')

class decrease_point(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    decrease_point = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(limit_value=100)],blank=False,verbose_name='扣除積分') 

class matchmaking(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    description = models.CharField(max_length = 400, default = None, blank = True, null = True,verbose_name = '專長')