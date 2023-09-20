from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class trust_point(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')
    trust_point = models.PositiveIntegerField(default=100,validators=[MaxValueValidator(limit_value=100)],null=False,blank=False,verbose_name='信用積分')

class matchmaking(models.Model):
    id = models.CharField(max_length= 10000,primary_key=True ,verbose_name = 'email')